# -*- coding: utf-8 -*-
# @Description :
# @File : bullet.py
# @Time : 2023/4/11 23:37
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddBulletForm(FlaskForm):
    user_id = IntegerField('user_id')
    etc_id = IntegerField('etc_id')
    msg = TextAreaField('Description', validators=[DataRequired(), Length(1, 254)])
    submit = SubmitField()
