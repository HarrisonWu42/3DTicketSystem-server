# -*- coding: utf-8 -*-
# @Description :
# @File : bullet.py
# @Time : 2023/4/11 23:33
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from datetime import datetime
from math import ceil

from flask import Blueprint, jsonify
from server.extensions import db
from server.models import Bullet, User, Etc
from server.forms.bullet import AddBulletForm


bullet_bp = Blueprint('bullet', __name__)


@bullet_bp.route('/write', methods=['POST'])
def write():
    form = AddBulletForm()
    user_id = form.user_id.data
    etc_id = form.etc_id.data
    msg = form.msg.data

    user = User.query.get(user_id)
    if user is None:
        return jsonify(code=403, message='User not exist.')
    etc = Etc.query.get(etc_id)
    if etc is None:
        return jsonify(code=403, message='Etc not exist.')

    bullet = Bullet(user_id=user_id, etc_id=etc_id, msg=msg)
    db.session.add(bullet)
    db.session.commit()

    return jsonify(code=200, message="Add bullet success.", data={'user_id': user_id,
                                                                  'user_name': user.name,
                                                                  'etc_id': etc_id,
                                                                  'etc_name': etc.name,
                                                                  'msg': msg})


@bullet_bp.route('/query/<etc_id>/<offset>/<page_size>', methods=['GET'])
def query(etc_id, offset, page_size):
    etc_id = int(etc_id)
    offset = int(offset)
    page_size = int(page_size)
    etc = Etc.query.get(etc_id)
    bullets = etc.etc_users

    page_bullets = bullets[(offset - 1) * page_size: offset * page_size]
    total_pages = ceil(len(bullets) / page_size)

    json_array = []
    for bullet in page_bullets:
        bullet_obj = {'user_id': bullet.user_id,
                      'etc_id': etc_id,
                      'etc_name': etc.name,
                      'msg': bullet.msg,
                      'create_timestamp': bullet.create_timestamp}
        json_array.append(bullet_obj)

    return jsonify(code=200, data={'bullet': json_array,
                                   'total_pages': total_pages,
                                   'bullet_num': len(page_bullets)})