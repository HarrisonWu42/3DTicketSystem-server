# -*- coding: utf-8 -*-
# @Description :
# @File : extensions.py
# @Time : 2023/3/13 0:51
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_moment import Moment
import threading
import redis
import requests


db = SQLAlchemy()
login_manager = LoginManager()
moment = Moment()


@login_manager.user_loader
def load_user(user_id):
    from server.models import User
    user = User.query.get(int(user_id))
    # session.permanent = True
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


# 定义一个Flask插件，用于监听Redis的过期键事件
class RedisExpiryListener(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        # print("here")
        # 获取Redis配置
        redis_host = app.config.get('REDIS_HOST')
        redis_port = app.config.get('REDIS_PORT')
        redis_db = app.config.get('REDIS_DB')

        # 连接到Redis实例
        self.redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

        # 监听Redis的过期键事件
        threading.Thread(target=self.listen_redis_expiry, daemon=True).start()

    # 监听Redis的过期键事件
    def listen_redis_expiry(self):
        pubsub = self.redis_conn.pubsub()
        pubsub.psubscribe("__keyevent@0__:expired")
        for message in pubsub.listen():
            if message['channel'] == b'__keyevent@0__:expired' and message['type'] == 'psubscribe':
                print(message)
            elif message['channel'] == b'__keyevent@0__:expired' and message['type'] == 'pmessage':
                print(message)
                data_key = message['data'].decode('utf-8')
                print(data_key)
                # 处理订单超时
                self.handle_timeout_order(data_key)

    # 处理订单超时的函数
    def handle_timeout_order(self, order_number):
        # 输出订单超时消息
        print(f'The order {order_number} is timeout，to cancel.')
        url = "http://127.0.0.1:5000/order/timeout"
        requests.post(url, json={'order_number': order_number})


redis_db = RedisExpiryListener()