# -*- coding: utf-8 -*-
# @Description :
# @File : seat.py
# @Time : 2023/4/9 17:37
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from datetime import datetime
from math import ceil

from flask import Blueprint, jsonify
from server.extensions import db
from server.models import Seat, Etc
from server.forms.seat import AddSeatForm, EditSeatForm, DeleteSeatForm
from server.utils import seats2json

seat_bp = Blueprint('seat', __name__)


# 添加座位
@seat_bp.route('/add', methods=['POST'])
def add():
    form = AddSeatForm()

    name = form.name.data
    type = form.type.data
    price = form.price.data
    etc_id = form.etc_id.data

    etc = Etc.query.get(etc_id)
    if etc is None:
        return jsonify(code=403, message="Etc not exist.")

    seat = Seat.query.filter_by(name=name, type=type, price=price, etc_id=etc_id).first()
    if seat is not None:
        return jsonify(code=401, message="Seat already exist.")

    seat = Seat(name=name, type=type, price=price)
    seat.etc = etc
    db.session.add(seat)
    db.session.commit()

    return jsonify(code=200, message="Add seat success.", data={'id': seat.id,
                                                                'name': seat.name,
                                                                'type': seat.type,
                                                                'create_timestamp': seat.create_timestamp,
                                                                'update_timestamp': seat.update_timestamp,
                                                                'price': seat.price,
                                                                'status': seat.status,
                                                                'etc_id': seat.etc_id})


# 修改座位
@seat_bp.route('/edit', methods=['POST'])
def edit():
    form = EditSeatForm()

    id = form.id.data
    name = form.name.data
    type = form.type.data
    price = form.price.data
    status = form.status.data

    seat = Seat.query.get(id)
    if seat is None:
        return jsonify(code=403, message="Seat not exist.")

    seat.name = name
    seat.type = type
    seat.price = price
    seat.status = status
    seat.update_timestamp = datetime.now()

    db.session.commit()

    return jsonify(code=200, message="Edit seat success.", data={'id': seat.id,
                                                                 'name': seat.name,
                                                                 'type': seat.type,
                                                                 'create_timestamp': seat.create_timestamp,
                                                                 'update_timestamp': seat.update_timestamp,
                                                                 'price': seat.price,
                                                                 'status': seat.status,
                                                                 'etc_id': seat.etc_id
                                                                 })


# 删除座位
@seat_bp.route('/delete', methods=['POST'])
def delete():
    form = DeleteSeatForm()
    id = form.id.data
    seat = Seat.query.get(id)

    if seat is None:
        return jsonify(code=403, message='Seat not exist.')

    db.session.delete(seat)
    db.session.commit()

    return jsonify(code=200, message='Delete seat success.', data={'id': seat.id,
                                                                   'name': seat.name,
                                                                   'type': seat.type,
                                                                   'create_timestamp': seat.create_timestamp,
                                                                   'update_timestamp': seat.update_timestamp,
                                                                   'price': seat.price,
                                                                   'status': seat.status,
                                                                   'etc_id': seat.etc_id})


# 获取座位信息
@seat_bp.route('/query/<seat_id>', methods=['GET'])
def query_seat_info(seat_id):
    seat_id = int(seat_id)
    seat = Seat.query.get(seat_id)

    if seat is None:
        return jsonify(code=403, message='Seat not exist.')

    return jsonify(code=200, message='Success.', data={'id': seat.id,
                                                                'name': seat.name,
                                                                'type': seat.type,
                                                                'create_timestamp': seat.create_timestamp,
                                                                'update_timestamp': seat.update_timestamp,
                                                                'price': seat.price,
                                                                'status': seat.status,
                                                                'etc_id': seat.etc_id
                                                       })


# 查询座位列表
@seat_bp.route('/query_by_etc/<etc_id>/<offset>/<page_size>', methods=['GET'])
def query_by_etc(etc_id, offset, page_size):
    etc_id = int(etc_id)
    page_size = int(page_size)
    offset = int(offset)

    etc = Etc.query.filter_by(id=etc_id).first()
    if etc is None:
        return jsonify(code=403, message='Etc not exist.')

    seats = Seat.query.filter_by(etc_id=etc_id).all()
    page_seats = seats[(offset - 1) * page_size: offset * page_size]
    total_pages = ceil(len(seats) / page_size)
    data = seats2json(page_seats)
    data['total_pages'] = total_pages
    data['seat_num'] = len(page_seats)

    return jsonify(code=200, data=data)


# 查询座位
@seat_bp.route('/search_by_name/<etc_id>/<seat_name>', methods=['GET'])
def search_by_name(etc_id, seat_name):
    etc_id = int(etc_id)
    seat = Seat.query.filter_by(name=seat_name, etc_id=etc_id).first()
    if seat is None:
        return jsonify(code=403, message='Seat not exist.')

    return jsonify(code=200, message='Success.', data={'id': seat.id,
                                                       'name': seat.name,
                                                       'type': seat.type,
                                                       'create_timestamp': seat.create_timestamp,
                                                       'update_timestamp': seat.update_timestamp,
                                                       'price': seat.price,
                                                       'status': seat.status,
                                                       'etc_id': seat.etc_id
                                                       })
