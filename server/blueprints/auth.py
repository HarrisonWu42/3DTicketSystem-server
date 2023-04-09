# -*- coding: utf-8 -*-
# @Description :
# @File : auth.py
# @Time : 2023/3/13 10:37
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask import redirect, url_for, Blueprint, make_response, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
# from server.emails import send_confirm_email, send_reset_password_email
from server.extensions import db
from server.forms.auth import LoginForm, RegisterForm
# from server.forms.auth import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from server.models import User
# from server.utils import generate_token, validate_token, extract_id_from_token
from server.decorators import confirm_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    # if current_user.is_authenticated:  # 是否登录
    #     return jsonify(code=303, message="Redirect to main page.")

    form = LoginForm()

    user = User.query.filter_by(name=form.name.data).first()
    if user is not None and user.deleted is False:
        if user.validate_password(form.password.data):
            if login_user(user):
                if user.type is 0:
                    role = "user"
                else:
                    role = "admin"
                return jsonify(code=200, message='Login success.', data={"id": user.id,
                                                                         "name": user.name,
                                                                         "role": role})
            else:
                return jsonify(code=400, message='Error, your account is blocked.')
        return jsonify(code=400, message='Error, invalid password.')

    return jsonify(code=302, message='Redirect to login page.')


# @auth_bp.route('/re-authenticate', methods=['GET', 'POST'])
# @login_required
# def re_authenticate():
#     if login_fresh():
#         return redirect(url_for('main.index'))
#
#     form = LoginForm()
#     if form.validate_on_submit() and current_user.validate_password(form.password.data):
#         confirm_login()
#         return redirect_back()x
#     # return render_template('auth/login.html', form=form)


@auth_bp.route('/logout', methods=['POST'])
# @login_required
def logout():
    logout_user()
    return jsonify(code=200, message='Logout success.')


@auth_bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify(code=303, message="Redirect to main page.")

    form = RegisterForm()

    user = User.query.filter_by(name=form.name.data).first()
    # user = User.query.filter_by(email=form.email.data.lower()).first()
    if user is not None:
        return jsonify(code=401, message="User already exist.")

    name = form.name.data
    # email = form.email.data.lower()
    password1 = form.password1.data
    password2 = form.password2.data
    if password1 != password2:
        return jsonify(code=402, message="Different password.")
    # user = User(name=name, email=email)
    user = User(name=name)
    user.set_password(password1)

    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(name=form.name.data).first()
    # user = User.query.filter_by(email=form.email.data.lower()).first()

    # token = generate_token(user=user, operation=Operations.CONFIRM)
    # url = 'http://localhost:8080/#' + url_for(endpoint='auth.confirm', token=token)
    # send_confirm_email(user?=user, url=url)

    return jsonify(code=200, message="Register success, redirect to login page.", data={"id": user.id})


# @auth_bp.route('/confirm/<token>', methods=['GET'])
# def confirm(token):
#
#     user_id = extract_id_from_token(token)
#     user = User.query.filter_by(id=user_id).first()
#
#     if user.confirmed:  # 已经确认过了，直接返回主页就可以了
#         return jsonify(code=303, message="Redirect to main page.")
#
#     if validate_token(user=user, token=token, operation=Operations.CONFIRM):
#         return jsonify(code=200, message="Confirm success.")
#     else:
#         return jsonify(code=400, message="Error, invalid or expired token.")
#
#
# @auth_bp.route('/resend-confirm-email', methods=['GET'])
# @login_required
# def resend_confirm_email():
#     if current_user.confirmed:
#         return jsonify(code=303, message="Redirect to main page.")
#
#     token = generate_token(user=current_user, operation=Operations.CONFIRM)
#     url = "http://localhost:8080/#" + url_for(endpoint='auth.confirm', token=token)
#
#     send_confirm_email(user=current_user, url=url)
#     return jsonify(code=303, message="Redirect to main page.")
#
#
# @auth_bp.route('/forget-password', methods=['GET'])
# def forget_password():
#     if current_user.is_authenticated:
#         return jsonify(code=303, message="Redirect to main page.")
#
#     form = ForgetPasswordForm()
#     if form.email.data is not None:
#         user = User.query.filter_by(email=form.email.data.lower()).first()
#         if user:
#             token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
#             url = "http://localhost:8080/#" + url_for(endpoint='auth.reset_password', token=token)
#
#             send_reset_password_email(user=user, url=url)
#             return jsonify(code=302, message="Redirect to login page.")
#         return jsonify(code=304, message="Redirect to forget_password page.", flash="Invalid email.")
#     return jsonify(code=305, message="Redirect to reset_password page.")
#
#
# @auth_bp.route('/reset-password/<token>', methods=['GET'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return jsonify(code=303, message="Redirect to main page.")
#
#     form = ResetPasswordForm()
#     if form.email.data is not None:
#         user = User.query.filter_by(email=form.email.data.lower()).first()
#         if user is None:
#             return jsonify(code=302, message="Redirect to reset_password page.", flash="Invalid email.")
#         if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD,
#                           new_password=form.password.data):
#             return jsonify(code=302, message="Redirect to login page.", flash="Password updated success.")
#         else:
#             return jsonify(code=305, message="Redirect to forget_password page.", flash="Invalid or expired link.")
#     return jsonify(code=305, message="Redirect to reset_password page.", form=form.data)
