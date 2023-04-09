# -*- coding: utf-8 -*-
# @Description :
# @File : auth.py
# @Time : 2023/3/20 15:28
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

from server.models import User


class LoginForm(FlaskForm):
    # email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    # email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data.lower()).first():
    #         raise ValidationError('The emails is already in use.')


# class ForgetPasswordForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
#     submit = SubmitField()
#
#
# class ResetPasswordForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
#     password = PasswordField('Password', validators=[
#         DataRequired(), Length(8, 128), EqualTo('password2')])
#     password2 = PasswordField('Confirm password', validators=[DataRequired()])
#     submit = SubmitField()