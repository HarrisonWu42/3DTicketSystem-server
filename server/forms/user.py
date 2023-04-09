# -*- coding: utf-8 -*-
# @Description :
# @File : user.py
# @Time : 2023/4/9 16:56
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class DeleteUserForm(FlaskForm):
    id = IntegerField('id')
    submit = SubmitField()