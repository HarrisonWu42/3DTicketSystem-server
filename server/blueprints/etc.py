# -*- coding: utf-8 -*-
# @Description :
# @File : etc.py
# @Time : 2023/4/9 17:39
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from datetime import datetime
from flask import Blueprint, jsonify
from server.extensions import db
from server.models import Etc
from server.forms.etc import AddEtcForm, EditEtcForm, DeleteEtcForm


etc_bp = Blueprint('etc', __name__)


# 添加场次
@etc_bp.route('/add', methods=['POST'])
def add():
    form = AddEtcForm()

    name = form.name.data
    description = form.description.data
    begin_timestamp = form.begin_timestamp.data
    end_timestamp = form.end_timestamp.data
    etc = Etc(name=name, description=description, begin_timestamp=begin_timestamp, end_timestamp=end_timestamp)

    db.session.add(etc)
    db.session.commit()

    etc = Etc.query.filter_by(name=name).first()

    return jsonify(code=200, message="Add etc success.", data={'id': etc.id,
                                                               'name': etc.name,
                                                               'description': etc.description,
                                                               'begin_timestamp': etc.begin_timestamp,
                                                               'end_timestamp': etc.end_timestamp,
                                                               'create_timestamp': etc.create_timestamp,
                                                               'update_timestamp': etc.update_timestamp})


# 修改场次
@etc_bp.route('/edit', methods=['POST'])
def edit():
    form = EditEtcForm()

    id = form.id.data
    name = form.name.data
    description = form.description.data
    begin_timestamp = form.begin_timestamp.data
    end_timestamp = form.end_timestamp.data

    etc = Etc.query.get(id)
    if etc is None:
        return jsonify(code=400, message="Etc not exist.")

    etc.name = name
    etc.description = description
    etc.begin_timestamp = begin_timestamp
    etc.end_timestamp = end_timestamp
    etc.update_timestamp = datetime.now()

    db.session.commit()

    return jsonify(code=200, message="Edit etc success.", data={'id': etc.id,
                                                                'name': etc.name,
                                                                'description': etc.description,
                                                                'begin_timestamp': etc.begin_timestamp,
                                                                'end_timestamp': etc.end_timestamp,
                                                                'create_timestamp': etc.create_timestamp,
                                                                'update_timestamp': etc.update_timestamp})


# 删除场次
@etc_bp.route('/delete', methods=['POST'])
def delete():
    form = DeleteEtcForm()
    id = form.id.data
    etc = Etc.query.get(id)

    if etc is None:
        return jsonify(code=403, message='Etc not exist.')

    db.session.delete(etc)
    db.session.commit()

    return jsonify(code=200, message='Delete etc success.', data={'id': etc.id,
                                                                   'name': etc.name,
                                                                   'description': etc.description,
                                                                   'begin_timestamp': etc.begin_timestamp,
                                                                   'end_timestamp': etc.end_timestamp,
                                                                   'create_timestamp': etc.create_timestamp,
                                                                   'update_timestamp': etc.update_timestamp})


# 查询场次详细信息
@etc_bp.route('/query/<etc_id>', methods=['GET'])
def query_etc_info(etc_id):
    etc_id = int(etc_id)
    etc = Etc.query.get(etc_id)

    if etc is None:
        return jsonify(code=403, message='Etc not exist.')

    return jsonify(code=200, message='Success.', data={'id': etc.id,
                                                       'name': etc.name,
                                                       'description': etc.description,
                                                       'begin_timestamp': etc.begin_timestamp,
                                                       'end_timestamp': etc.end_timestamp,
                                                       'create_timestamp': etc.create_timestamp,
                                                       'update_timestamp': etc.update_timestamp})


# 查询场次列表（根据时间）
@etc_bp.route('/x4', methods=['GET'])
def x4():
    pass


# 搜索场次（根据名字）
@etc_bp.route('/search_by_name/<etc_name>', methods=['GET'])
def search_by_name(etc_name):
    etc = Etc.query.filter_by(name=etc_name).first()
    if etc is None:
        return jsonify(code=403, message='Etc not exist.')

    return jsonify(code=200, message='Success.', data={'id': etc.id,
                                                       'name': etc.name,
                                                       'description': etc.description,
                                                       'begin_timestamp': etc.begin_timestamp,
                                                       'end_timestamp': etc.end_timestamp,
                                                       'create_timestamp': etc.create_timestamp,
                                                       'update_timestamp': etc.update_timestamp})