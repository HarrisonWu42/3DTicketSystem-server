# -*- coding: utf-8 -*-
# @Description :
# @File : cart.py
# @Time : 2023/4/11 15:35
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class AddCartForm(FlaskForm):
    user_id = IntegerField('user_id')
    etc_id = IntegerField('etc_id')
    seat_id = IntegerField('seat_id')
    submit = SubmitField()


class EditCartForm(FlaskForm):
    seat_ids = StringField('seat_ids')
    select_statuses = StringField('select_statuses')
    submit = SubmitField()


class DeleteCartForm(FlaskForm):
    seat_id = IntegerField('seat_id')
    submit = SubmitField()


class DeleteCartsForm(FlaskForm):
    seat_ids = StringField('seat_ids')
    submit = SubmitField()