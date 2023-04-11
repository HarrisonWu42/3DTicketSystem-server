# -*- coding: utf-8 -*-
# @Description :
# @File : etc.py
# @Time : 2023/4/9 18:50
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length


class AddEtcForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 30)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 254)])
    begin_timestamp = DateTimeField('begin_timestamp')
    end_timestamp = DateTimeField('begin_timestamp')
    submit = SubmitField()


class EditEtcForm(FlaskForm):
    id = IntegerField('id')
    name = StringField('name', validators=[DataRequired(), Length(1, 30)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(1, 254)])
    begin_timestamp = DateTimeField('begin_timestamp')
    end_timestamp = DateTimeField('begin_timestamp')
    submit = SubmitField()


class DeleteEtcForm(FlaskForm):
    id = IntegerField('id')
    submit = SubmitField()