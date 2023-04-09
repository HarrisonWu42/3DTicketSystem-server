# -*- coding: utf-8 -*-
# @Description :
# @File : admin.py
# @Time : 2023/3/20 15:28
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class EditRoleForm(FlaskForm):
    role = StringField('Role')
    submit = SubmitField()