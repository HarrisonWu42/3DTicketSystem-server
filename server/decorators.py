# -*- coding: utf-8 -*-
# @Description :
# @File : decorators.py
# @Time : 2023/3/13 0:58
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from functools import wraps

from flask import abort, jsonify
from flask_login import current_user


def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            # message = Markup(
            #     'Please confirm your account first.'
            #     'Not receive the email?'
            #     '<a class="alert-link" href="%s">Resend Confirm Email</a>' %
            #     url_for('auth.resend_confirm_email'))
            # flash(message, 'warning')
            return jsonify(code=303, message="Redirect to main page.", flash='Please confirm your account first.\n'
                                                                             'Not receive the email?\n'
                                                                             '<a class="alert-link" href="%s">Resend Confirm Email</a>' % 'auth.resend_confirm_email')
        return func(*args, **kwargs)
    return decorated_function


def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission_name):
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(func):
    return permission_required('ADMINISTER')(func)