# -*- coding: utf-8 -*-
# @Description :
# @File : order.py
# @Time : 2023/4/10 18:30
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm
import json
from datetime import datetime
from math import ceil
from flask import Blueprint, jsonify, request
from server.extensions import db, RedisExpiryListener, redis_db
from server.models import Ticket, Seat, Order, User, Cart
from server.forms.order import AddOrderForm, EditOrderForm, DeleteOrderForm, PayOrderForm
from server.utils import generate_order_number, tickets2json, orders2json, alipay_obj, datetime2string, string2datetime
from server.settings import ALIPAY_SETTING


order_bp = Blueprint('order', __name__)


# def handle_timeout_order(self, order_number):
#     # 输出订单超时消息
#     print(f'Rewrite {order_number} is timeout，already cancel.')
#     order = Order.query.filter_by(order_number=order_number).first()
#     self.db.session.delete(order)
#     self.db.session.commit()
# RedisExpiryListener.handle_timeout_order = handle_timeout_order


@order_bp.route('/timeout', methods=['POST'])
def timeout():
    res = request.get_json()
    order_number = res.get("order_number")
    # print("timeout: ", order_number)
    order = Order.query.filter_by(order_number=order_number).first()

    data = tickets2json(order.tickets)
    data['user_id'] = order.user_id
    data['order_number'] = order_number
    data['total'] = order.total
    data['status'] = order.status
    data['create_timestamp'] = order.create_timestamp
    data['update_timestamp'] = order.update_timestamp
    data['ticket num'] = len(order.tickets)

    for ticket in order.tickets:
        seat_id = ticket.seat_id
        seat = Seat.query.get(seat_id)
        seat.status = 2
        db.session.delete(ticket)

    db.session.delete(order)
    db.session.commit()

    return jsonify(code=200, message="The order timeout", data=data)


# 生成订单
@order_bp.route('/add', methods=['POST'])
def add():
    form = AddOrderForm()

    user_id = form.user_id.data
    seat_id_list = form.seat_ids.data.split(',')

    user = User.query.get(user_id)
    if user is None:
        return jsonify(code=403, message='User not exist.')

    order_number = generate_order_number()
    while Order.query.filter_by(order_number=order_number).first() is not None:
        order_number = generate_order_number()

    seat_list = []
    total = 0
    for i in range(len(seat_id_list)):
        seat_id_list[i] = int(seat_id_list[i])
        seat_id = seat_id_list[i]
        seat = Seat.query.get(seat_id)
        seat_list.append(seat)
        total += seat.price
        cart = Cart.query.get((user_id, seat_id))
        db.session.delete(cart)

    order = Order(user_id=user_id, order_number=order_number, total=total)

    db.session.add(order)

    ticket_list = []
    for seat in seat_list:
        seat.status = 1
        ticket = Ticket(order_number=order_number,
                        etc_id=seat.etc.id,
                        etc_name=seat.etc.name,
                        begin_timestamp=seat.etc.begin_timestamp,
                        end_timestamp=seat.etc.end_timestamp,
                        seat_id=seat.id,
                        seat_name=seat.name,
                        seat_type=seat.type,
                        price=seat.price)
        ticket_list.append(ticket)
        db.session.add(ticket)

    db.session.commit()

    redis_db.redis_conn.setex(order_number, 15*60, datetime2string(order.create_timestamp))

    data = tickets2json(ticket_list)
    data['user_id'] = user_id
    data['order_number'] = order_number
    data['total'] = total
    data['create_timestamp'] = order.create_timestamp
    data['ticket num'] = len(ticket_list)
    return jsonify(code=200, message="Add order success.", data=data)


# 修改订单状态（取消订单）
@order_bp.route('/edit', methods=['POST'])
def edit():
    form = EditOrderForm()

    order_number = form.order_number.data
    order = Order.query.filter_by(order_number=order_number).first()
    if order is None:
        return jsonify(code=403, message='Order not exist.')

    order.status = 2  # 取消订单
    order.update_timestamp = datetime.now()
    for ticket in order.tickets:
        seat = Seat.query.get(ticket.seat_id)
        seat.status = 2     # 取消座位的锁定
        seat.update_timestamp = datetime.now()

    db.session.commit()

    data = tickets2json(order.tickets)
    data['user_id'] = order.user_id
    data['order_number'] = order_number
    data['total'] = order.total
    data['status'] = order.status
    data['create_timestamp'] = order.create_timestamp
    data['update_timestamp'] = order.update_timestamp
    data['ticket num'] = len(order.tickets)

    return jsonify(code=200, message="Edit order success.", data=data)


# 删除订单
@order_bp.route('/delete', methods=['POST'])
def delete():
    form = DeleteOrderForm()

    order_number = form.order_number.data
    order = Order.query.filter_by(order_number=order_number).first()
    if order is None:
        return jsonify(code=403, message='Order not exist.')
    if order.status is 0:
        return jsonify(code=406, message='The order has not been paid or canceled, please check the order status.')

    for ticket in order.tickets:
        db.session.delete(ticket)
    db.session.delete(order)
    db.session.commit()

    data = tickets2json(order.tickets)
    data['user_id'] = order.user_id
    data['order_number'] = order_number
    data['total'] = order.total
    data['status'] = order.status
    data['create_timestamp'] = order.create_timestamp
    data['update_timestamp'] = order.update_timestamp
    data['ticket num'] = len(order.tickets)

    return jsonify(code=200, message="Delete order success.", data=data)


# 查询订单列表
@order_bp.route('/query/<user_id>/<offset>/<page_size>', methods=['GET'])
def query(user_id, offset, page_size):
    user_id = int(user_id)
    page_size = int(page_size)
    offset = int(offset)
    user = User.query.get(user_id)
    if user is None:
        return jsonify(code=403, message='User not exist.')

    orders = user.orders
    page_orders = orders[(offset - 1) * page_size: offset * page_size]
    total_pages = ceil(len(orders) / page_size)
    data = orders2json(page_orders)
    data['total_pages'] = total_pages
    data['order_num'] = len(page_orders)

    return jsonify(code=200, data=data)


# 查询订单详情
@order_bp.route('/query_info/<order_number>', methods=['GET'])
def query_info(order_number):
    order = Order.query.filter_by(order_number=order_number).first()
    tickets = order.tickets

    data = tickets2json(tickets)
    data['user_id'] = order.user_id
    data['order_number'] = order_number
    data['total'] = order.total
    data['status'] = order.status
    data['create_timestamp'] = order.create_timestamp
    data['update_timestamp'] = order.update_timestamp
    data['ticket number'] = len(tickets)
    return jsonify(code=200, data=data)


# 支付功能
@order_bp.route('/pay', methods=['POST'])
def pay():
    form = PayOrderForm()

    order_number = form.order_number.data
    order = Order.query.filter_by(order_number=order_number).first()
    if order is None:
        return jsonify(code=403, message='Order not exist.')
    tickets = order.tickets
    data = tickets2json(tickets)
    data['user_id'] = order.user_id
    data['order_number'] = order_number
    data['total'] = order.total
    data['status'] = order.status
    data['create_timestamp'] = order.create_timestamp
    data['update_timestamp'] = order.update_timestamp
    data['ticket number'] = len(tickets)

    alipay = alipay_obj()
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_number,  # 商品订单号  唯一的
        total_amount=order.total,  # 商品价格
        subject='3DTicketSystem',  # 商品的名称
        return_url=ALIPAY_SETTING.get('ALIPAY_RETURN_URL'),  # 同步回调网址--用于前端，付成功之后回调
        notify_url=ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL')  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容
    )
    # 我这里大概讲一下为什么要有同步/异步，因为同步是前端的，
    # 如果前端出现页面崩了，那么校验有后端完成，
    # 而且在实际开发中，后端一定要校验，因为前端的校验，可被修改
    url = 'https://openapi.alipaydev.com/gateway.do' + '?' + order_string
    return jsonify(code=200, url=url, data=data)


# 支付成功回调
@order_bp.route('/pay/result/', methods=['GET', 'POST'])
def pay_result():
    charset = request.args.get('charset')
    out_trade_no = request.args.get('out_trade_no')
    method = request.args.get('method')
    total_amount = request.args.get('total_amount')
    sign = request.args.get('sign')
    trade_no = request.args.get('trade_no')
    auth_app_id = request.args.get('auth_app_id')
    version = request.args.get('version')
    app_id = request.args.get('app_id')
    sign_type = request.args.get('sign_type')
    seller_id = request.args.get('seller_id')
    timestamp = request.args.get('timestamp')
    data = {'charset': charset, 'out_trade_no': out_trade_no, 'method': method, 'total_amount': total_amount,
            'sign': sign, 'trade_no': trade_no, 'auth_app_id': auth_app_id, 'version': version, 'app_id': app_id,
            'sign_type': sign_type, 'seller_id': seller_id, 'timestamp': timestamp}

    # 同步回调
    if request.method == "GET":
        # 进行校验，因为支付成功之后，后端是不知道是否成功的，所以需要校验一下
        alipay = alipay_obj()
        signature = data.pop("sign")
        # verification
        success = alipay.verify(data, signature)  # success ----> True False
        order = Order.query.filter_by(order_number=out_trade_no).first()
        if success is True:     # 支付成功，要写逻辑了
            order.status = 1
            tickets = order.tickets
            for ticket in tickets:
                ticket.status = 1
            db.session.commit()
            return jsonify(code=200, message='Pay success. Synchronous callback.')
        return jsonify(code=200, message='Pay failed.')

    # 异步回调，当你前端页面崩了以后，支付宝会向该路由，发送post请求，这个是间隔发8次，如果没有返回success
    alipay = alipay_obj()
    signature = data.pop("sign")
    success = alipay.verify(data, signature)  # True False
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        print('pay success')
        return jsonify(code=200, message='Pay success. Asynchronous callback.')
    return jsonify(code=200, message='Pay failed.')


