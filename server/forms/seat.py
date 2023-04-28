# -*- coding: utf-8 -*-
# @Description :
# @File : seat.py
# @Time : 2023/4/9 17:37
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddSeatForm(FlaskForm):
    etc_id = IntegerField('etc_id')
    name = StringField('name', validators=[DataRequired(), Length(1, 30)])
    type = StringField('type', validators=[DataRequired(), Length(1, 30)])
    price = IntegerField('price')
    submit = SubmitField()


class EditSeatForm(FlaskForm):
    id = IntegerField('id')
    name = StringField('name', validators=[DataRequired(), Length(1, 30)])
    type = StringField('type', validators=[DataRequired(), Length(1, 30)])
    price = IntegerField('price')
    status = IntegerField('status')
    submit = SubmitField()


class DeleteSeatForm(FlaskForm):
    id = IntegerField('id')
    submit = SubmitField()