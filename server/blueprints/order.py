# -*- coding: utf-8 -*-
# @Description :
# @File : order.py
# @Time : 2023/4/10 18:30
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from datetime import datetime
from flask import Blueprint, jsonify
from server.extensions import db
from server.models import Etc
from server.forms.etc import AddEtcForm, EditEtcForm, DeleteEtcForm


order_bp = Blueprint('order', __name__)


# 生成订单
@order_bp.route('/add', methods=['POST'])
def add():
    return jsonify(code=200, message="Add cart success.", data={})


# 修改订单状态
@order_bp.route('/edit', methods=['POST'])
def edit():
    return jsonify(code=200, message="Add cart success.", data={})


# 删除订单
@order_bp.route('/detele', methods=['POST'])
def detele():
    return jsonify(code=200, message="Add cart success.", data={})


# 查询订单列表
@order_bp.route('/query', methods=['GET'])
def query():
    return jsonify(code=200, message="Add cart success.", data={})


# 查询订单详情
@order_bp.route('/query_info', methods=['POST'])
def query_info():
    return jsonify(code=200, message="Add cart success.", data={})


# 支付功能
@order_bp.route('/pay', methods=['POST'])
def pay():
    return jsonify(code=200, message="Add cart success.", data={})


