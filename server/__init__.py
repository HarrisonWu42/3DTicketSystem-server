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
from server.extensions import db
from server.models import User


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
    # login_manager.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    # flask_excel.init_excel(app)


def register_blueprints(app):
    # app.register_blueprint(home_bp, url_prefix='/home')
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    # app.register_blueprint(admin_bp, url_prefix='/admin')
    # app.register_blueprint(task_bp, url_prefix='/task')
    # app.register_blueprint(taskset_bp, url_prefix='/taskset')
    # app.register_blueprint(group_bp, url_prefix='/group')
    # app.register_blueprint(project_bp, url_prefix='/project')


def regitser_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)