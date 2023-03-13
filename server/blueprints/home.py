# -*- coding: utf-8 -*-
# @Description :
# @File : home.py
# @Time : 2023/3/13 11:09
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask import Blueprint, jsonify
from sqlalchemy import func
from server.extensions import db
from server.models import User

home_bp = Blueprint('home', __name__)


@home_bp.route('/', methods=['GET'])
def show_datas():
    # user_num = db.session.query(func.count(User.id)).first()
    user_num = User.query.count()
    return jsonify(code=200, data={"user_num": user_num})
