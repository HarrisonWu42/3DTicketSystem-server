# -*- coding: utf-8 -*-
# @Description :
# @File : cart.py
# @Time : 2023/4/10 18:30
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from datetime import datetime
from flask import Blueprint, jsonify
from server.extensions import db
from server.models import Cart, User, Etc, Seat
from server.forms.cart import AddCartForm, EditCartForm, DeleteCartForm, DeleteCartsForm

cart_bp = Blueprint('cart', __name__)


# 添加到购物车
@cart_bp.route('/add', methods=['POST'])
def add():
    form = AddCartForm()

    user_id = form.user_id.data
    etc_id = form.etc_id.data
    seat_id = form.seat_id.data

    user = User.query.get(user_id)
    if user is None:
        return jsonify(code=403, message='User not exist.')

    etc = Etc.query.get(etc_id)
    if etc is None:
        return jsonify(code=403, message='Etc not exist.')

    seat = Seat.query.get(seat_id)
    if seat is None:
        return jsonify(code=403, message='Seat not exist.')
    elif seat.status < 2:
        return jsonify(code=405, message='Seat can not by choose')

    cart = Cart.query.get((user_id, seat_id))
    if cart is not None:
        return jsonify(code=200, message="Cart exist.")

    cart = Cart(user_id=user_id, seat_id=seat_id, etc_id=etc_id)
    db.session.add(cart)
    db.session.commit()

    return jsonify(code=200, message="Add cart success.", data={'user_id': user_id,
                                                                'user_name': user.name,
                                                                'etc_id': etc_id,
                                                                'etc_name': etc.name,
                                                                'begin_timestamp': etc.begin_timestamp,
                                                                'end_timestamp': etc.end_timestamp,
                                                                'seat_id': seat_id,
                                                                'seat_name': seat.name,
                                                                'type': seat.type,
                                                                'price': seat.price})


# 查询某个用户的购物车列表
@cart_bp.route('/query/<user_id>', methods=['GET'])
def query_cart(user_id):
    user_id = int(user_id)
    user = User.query.get(user_id)
    carts = user.user_seats
    json_array = []
    for cart in carts:
        etc_id = cart.etc_id
        etc = Etc.query.get(etc_id)
        if etc is None:
            pass
        seat_id = cart.seat_id
        seat = Seat.query.get(seat_id)
        if seat is None or seat.status < 2:
            pass
        cart_obj = {'user_id': user_id,
                    'etc_id': etc_id,
                    'etc_name': etc.name,
                    'begin_timestamp': etc.begin_timestamp,
                    'end_timestamp': etc.end_timestamp,
                    'seat_id': seat_id,
                    'seat_name': seat.name,
                    'type': seat.type,
                    'price': seat.price,
                    'select_status': cart.select_status}
        json_array.append(cart_obj)

    return jsonify(code=200, message="Success.", data={'cart': json_array})


# 更新某个用户的购物车列表商品的选中状态
@cart_bp.route('/edit/<user_id>', methods=['POST'])
def edit(user_id):
    user_id = int(user_id)
    user = User.query.get(user_id)
    carts = user.user_seats

    form = EditCartForm()

    seat_ids = form.seat_ids.data
    select_statuses = form.select_statuses.data

    seat_id_list = seat_ids.split(',')
    select_status_list = select_statuses.split(',')
    for i in range(len(seat_id_list)):
        seat_id_list[i] = int(seat_id_list[i])
        select_status_list[i] = int(select_status_list[i])

    for cart in carts:
        seat_id = cart.seat_id
        if seat_id in seat_id_list:
            idx = seat_id_list.index(seat_id)
            cart.select_status = select_status_list[idx]
            cart.update_timestamp = datetime.now()

    db.session.commit()

    json_array = []
    for cart in carts:
        etc_id = cart.etc_id
        etc = Etc.query.get(etc_id)
        seat_id = cart.seat_id
        seat = Seat.query.get(seat_id)
        cart_obj = {'user_id': user_id,
                    'etc_id': etc_id,
                    'etc_name': etc.name,
                    'begin_timestamp': etc.begin_timestamp,
                    'end_timestamp': etc.end_timestamp,
                    'seat_id': seat_id,
                    'seat_name': seat.name,
                    'type': seat.type,
                    'price': seat.price,
                    'select_status': cart.select_status}
        json_array.append(cart_obj)

    return jsonify(code=200, message="Success.", data={'cart': json_array})


# 全选/全不选
@cart_bp.route('/select_all/<user_id>/<option>', methods=['POST'])
def select_all_none(user_id, option):
    user_id = int(user_id)
    option = int(option)
    user = User.query.get(user_id)
    carts = user.user_seats

    for cart in carts:
        cart.select_status = option
        cart.update_timestamp = datetime.now()

    db.session.commit()

    json_array = []
    for cart in carts:
        etc_id = cart.etc_id
        etc = Etc.query.get(etc_id)
        seat_id = cart.seat_id
        seat = Seat.query.get(seat_id)
        cart_obj = {'user_id': user_id,
                    'etc_id': etc_id,
                    'etc_name': etc.name,
                    'begin_timestamp': etc.begin_timestamp,
                    'end_timestamp': etc.end_timestamp,
                    'seat_id': seat_id,
                    'seat_name': seat.name,
                    'type': seat.type,
                    'price': seat.price,
                    'select_status': cart.select_status}
        json_array.append(cart_obj)

    return jsonify(code=200, message="Success.", data={'cart': json_array})


# 删除购物车原本在购物车里面的某个票:只删一个
@cart_bp.route('/delete/<user_id>', methods=['POST'])
def delete(user_id):
    user_id = int(user_id)
    form = DeleteCartForm()
    seat_id = form.seat_id.data
    cart = Cart.query.get((user_id, seat_id))
    etc_id = cart.etc_id
    etc = Etc.query.get(etc_id)
    seat_id = cart.seat_id
    seat = Seat.query.get(seat_id)

    if cart is None:
        return jsonify(code=403, message='Cart not exist.')

    db.session.delete(cart)
    db.session.commit()

    return jsonify(code=200, message="Delete cart success.", data={'user_id': user_id,
                                                                   'etc_id': etc_id,
                                                                   'etc_name': etc.name,
                                                                   'begin_timestamp': etc.begin_timestamp,
                                                                   'end_timestamp': etc.end_timestamp,
                                                                   'seat_id': seat_id,
                                                                   'seat_name': seat.name,
                                                                   'type': seat.type,
                                                                   'price': seat.price})


# 删除购物车原本在购物车里面的某个票:批量删除
@cart_bp.route('/delete_some/<user_id>', methods=['POST'])
def delete_some(user_id):
    user_id = int(user_id)
    form = DeleteCartsForm()
    seat_id_list = form.seat_ids.data.split(',')

    json_array = []
    for seat_id in seat_id_list:
        seat_id = int(seat_id)
        cart = Cart.query.get((user_id, seat_id))
        etc_id = cart.etc_id
        etc = Etc.query.get(etc_id)
        seat_id = cart.seat_id
        seat = Seat.query.get(seat_id)

        if cart is None:
            pass

        cart_obj = {'user_id': user_id,
                    'etc_id': etc_id,
                    'etc_name': etc.name,
                    'begin_timestamp': etc.begin_timestamp,
                    'end_timestamp': etc.end_timestamp,
                    'seat_id': seat_id,
                    'seat_name': seat.name,
                    'type': seat.type,
                    'price': seat.price}
        json_array.append(cart_obj)

        db.session.delete(cart)
    db.session.commit()

    return jsonify(code=200, message="Delete carts success.", data={'cart': json_array})