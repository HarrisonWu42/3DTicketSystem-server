# -*- coding: utf-8 -*-
# @Description :
# @File : order.py
# @Time : 2023/4/15 21:05
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField


class AddOrderForm(FlaskForm):
    user_id = IntegerField('user_id')
    # etc_ids = StringField('etc_ids')
    seat_ids = StringField('seat_ids')
    submit = SubmitField()


class EditOrderForm(FlaskForm):
    order_number = StringField('order_number')
    submit = SubmitField()


class DeleteOrderForm(FlaskForm):
    order_number = StringField('order_number')
    submit = SubmitField()


class PayOrderForm(FlaskForm):
    order_number = StringField('order_number')
    submit = SubmitField()