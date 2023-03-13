# -*- coding: utf-8 -*-
# @Description :
# @File : extensions.py
# @Time : 2023/3/13 0:51
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
# from flask_mail import Mail
from flask_moment import Moment

db = SQLAlchemy()
login_manager = LoginManager()
# mail = Mail()
moment = Moment()


@login_manager.user_loader
def load_user(user_id):
    from server.models import User
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'

login_manager.refresh_view = 'auth.re_authenticate'
# login_manager.needs_refresh_message = 'Your custom message'
login_manager.needs_refresh_message_category = 'warning'


class Guest(AnonymousUserMixin):
    def can(self, permission_name):
        return False

    @property
    def is_admin(self):
        return False


login_manager.anonymous_user = Guest