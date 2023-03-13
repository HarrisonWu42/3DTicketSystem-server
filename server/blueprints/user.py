# -*- coding: utf-8 -*-
# @Description :
# @File : user.py
# @Time : 2023/3/13 10:36
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask import current_app, jsonify, Blueprint, url_for

from server.models import User
from server.extensions import db
from server.utils import generate_token, extract_id_from_token, validate_token


user_bp = Blueprint('user', __name__)