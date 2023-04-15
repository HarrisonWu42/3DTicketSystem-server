# -*- coding: utf-8 -*-
# @Description :
# @File : utils.py
# @Time : 2023/4/9 16:37
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


import random
import string
from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig
from server.settings import ALIPAY_SETTING


def generate_order_number():
    return ''.join(random.choices(string.digits, k=30))


# 生成支付alipay对象，以供调用
def alipay_obj():
    alipay = AliPay(
        appid=ALIPAY_SETTING.get('ALIPAY_APP_ID'),
        app_notify_url=None,  # 默认回调 url
        app_private_key_string=open(ALIPAY_SETTING.get('APP_PRIVATE_KEY_STRING')).read(),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=open(ALIPAY_SETTING.get('ALIPAY_PUBLIC_KEY_STRING')).read(),
        sign_type=ALIPAY_SETTING.get('SIGN_TYPE'),  # RSA 或者 RSA2
        debug=ALIPAY_SETTING.get('ALIPAY_DEBUG'),  # 默认 False
        verbose=False,  # 输出调试数据
        # config=AliPayConfig(timeout=50)  # 可选，请求超时时间
    )
    return alipay


def users2json(users):
    json_array = []
    for user in users:
        role = 'user'
        if user.is_admin is True:
            role = 'admin'

        user_obj = {'id': user.id,
                    'name': user.name,
                    'role': role,
                    'create_timestamp': user.create_timestamp,
                    'update_timestamp': user.update_timestamp}
        json_array.append(user_obj)
    json_dic = {"users": json_array}

    return json_dic


def medias2json(medias):
    json_array = []
    for media in medias:
        media_obj = {'id': media.id,
                     'name': media.name,
                     'type': media.type,
                     'url': media.url,
                     'etc_id': media.etc_id,
                     'create_timestamp': media.create_timestamp,
                     'update_timestamp': media.update_timestamp}
        json_array.append(media_obj)
    json_dic = {"medias": json_array}

    return json_dic


def seats2json(seats):
    json_array = []
    for seat in seats:
        seat_obj = {'id': seat.id,
                    'name': seat.name,
                    'type': seat.type,
                    'create_timestamp': seat.create_timestamp,
                    'update_timestamp': seat.update_timestamp,
                    'price': seat.price,
                    'status': seat.status,
                    'etc_id': seat.etc_id}
        json_array.append(seat_obj)
    json_dic = {"seats": json_array}

    return json_dic


def etcs2json(etcs):
    json_array = []
    for etc in etcs:
        etc_obj = {'id': etc.id,
                   'name': etc.name,
                   'description': etc.description,
                   'begin_timestamp': etc.begin_timestamp,
                   'end_timestamp': etc.end_timestamp,
                   'create_timestamp': etc.create_timestamp,
                   'update_timestamp': etc.update_timestamp}
        json_array.append(etc_obj)
    json_dic = {"etcs": json_array}

    return json_dic


def tickets2json(tickets):
    json_array = []
    for ticket in tickets:
        ticket_obj = {'id': ticket.id,
                      'etc_id': ticket.etc_id,
                      'etc_name': ticket.etc_name,
                      'begin_timestamp': ticket.begin_timestamp,
                      'end_timestamp': ticket.end_timestamp,
                      'seat_id': ticket.seat_id,
                      'seat_name': ticket.seat_name,
                      'seat_type': ticket.seat_type,
                      'price': ticket.price}
        json_array.append(ticket_obj)
    json_dic = {"tickets": json_array}

    return json_dic


def orders2json(orders):
    json_array = []
    for order in orders:
        order_obj = {'order_number': order.order_number,
                     'total': order.total,
                     'ticket number': len(order.tickets),
                     'status': order.status,
                     'create_timestamp': order.create_timestamp,
                     'update_timestamp': order.update_timestamp}
        json_array.append(order_obj)
    json_dic = {"orders": json_array}

    return json_dic

