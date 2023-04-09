# -*- coding: utf-8 -*-
# @Description :
# @File : user.py
# @Time : 2023/3/13 10:36
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from math import ceil
from flask import current_app, jsonify, Blueprint, url_for
from server.models import User
from server.extensions import db
from server.utils import users2json
from server.forms.user import DeleteUserForm

user_bp = Blueprint('user', __name__)


# 获取用户信息（个人）
@user_bp.route('/query/<user_id>', methods=['GET'])
def query_user_info(user_id):
    user_id = int(user_id)
    user = User.query.filter_by(id=user_id).first()
    role = 'user'
    if user.is_admin is True:
        role = 'admin'

    return jsonify(code=200, message='Success.', data={"id": user.id,
                                                       "name": user.name,
                                                       "role": role
                                                       })


# 获取用户列表（管理员）
# 这个user_id是当前用户，检查是不是管理员用的
@user_bp.route('/query_users/<user_id>/<offset>/<page_size>', methods=['GET'])
def query_user_list(user_id, offset, page_size):
    user_id = int(user_id)
    page_size = int(page_size)
    offset = int(offset)

    user = User.query.filter_by(id=user_id).first()
    if user.is_admin is False:
        return jsonify(code=401, message='Insufficient authority.')

    users = User.query.filter_by(deleted=0).all()
    page_users = users[(offset - 1) * page_size: offset * page_size]
    total_pages = ceil(len(users) / page_size)
    data = users2json(page_users)
    data['total_pages'] = total_pages
    data['user_num'] = len(page_users)

    return jsonify(code=200, data=data)


# 查询用户（根据name）， search
@user_bp.route('/search/<user_name>', methods=['GET'])
def search_user(user_name):
    user = User.query.filter_by(name=user_name, deleted=0).first()
    if user is None:
        return jsonify(code=403, message='User not exist.')

    role = 'user'
    if user.is_admin is True:
        role = 'admin'

    return jsonify(code=200, message='Success.', data={"id": user.id,
                                                       "name": user.name,
                                                       "role": role
                                                       })


# 删除用户
@user_bp.route('/delete', methods=['POST'])
def delete():
    form = DeleteUserForm()
    id = form.id.data
    user = User.query.get(id)

    if user is None or user.is_deleted is True:
        return jsonify(code=403, message='User not exist.')

    role = 'user'
    if user.is_admin is True:
        role = 'admin'

    detele_timestamp = user.delete()
    db.session.commit()

    return jsonify(code=200, message='Delete user success.', data={'id': user.id,
                                                                   'name': user.name,
                                                                   'role': role,
                                                                   'create_timestamp': user.create_timestamp,
                                                                   'update_timestamp': user.update_timestamp,
                                                                   'delete_timestamp': detele_timestamp
                                                                   })