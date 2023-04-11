# -*- coding: utf-8 -*-
# @Description :
# @File : __init__.py.py
# @Time : 2023/3/13 0:49
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


import os
from flask import Flask
from flask_cors import CORS
from flask_login import current_user
from server.extensions import db, login_manager
from server.models import User
from server.blueprints.user import user_bp
from server.blueprints.auth import auth_bp
from server.blueprints.seat import seat_bp
from server.blueprints.etc import etc_bp
from server.blueprints.media import media_bp
from server.blueprints.openai import openai_bp
from server.blueprints.cart import cart_bp
from server.blueprints.bullet import bullet_bp
from server.blueprints.order import order_bp


def create_app(config_name=None):
    # if config_name is None:
    #     config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('server')
    CORS(app, supports_credentials=True)

    app.config.from_pyfile('settings.py')

    register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册拓展
    register_blueprints(app)  # 注册蓝本
    regitser_shell_context(app)  # 注册shell上下文处理函数
    return app


def register_logging(app):
    pass


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    # flask_excel.init_excel(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(seat_bp, url_prefix='/seat')
    app.register_blueprint(etc_bp, url_prefix='/etc')
    app.register_blueprint(openai_bp, url_prefix='/openai')
    app.register_blueprint(media_bp, url_prefix='/media')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(bullet_bp, url_prefix='/bullet')
    app.register_blueprint(order_bp, url_prefix='/order')


def regitser_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)