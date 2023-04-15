# -*- coding: utf-8 -*-
# @Description :
# @File : settings.py
# @Time : 2023/3/13 0:50
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


import os
import sys


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


"""
    Database
"""
# 'mysql+pymysql://用户名称:密码@localhost:端口/数据库名称'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/tickets'
SQLALCHEMY_TRACK_MODIFICATIONS = True


SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

# """
#     Email
# """
# MAIL_SERVER = 'smtp.qq.com'
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USE_TLS = False
# MAIL_USERNAME = 'hangzhouwh@qq.com'
# ADMIN_EMAIL = MAIL_USERNAME
# TEACHER_EMAIL = 'zucc.edu.cn'
# MAIL_PASSWORD = 'xopwpdloezkvcaig'  # qq邮箱授权码
# MAIL_DEFAULT_SENDER = ('ScratchAi Admin', MAIL_USERNAME)
# SCRATCHAI_MAIL_SUBJECT_PREFIX = '[scratchai]'
#
# FILE_FOLDER = 'path/to/file_folder'
# ALLOWED_FILETYPES = set(['sb3'])


"""
    OPENAI
"""
OPENAI_API_KEY = "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"


"""
    ALIPAY
"""
# 支付宝配置
# 支付宝支付相关配置
ALIPAY_SETTING = {
    'ALIPAY_APP_ID': "2021000122679309",  # 应用ID(上线之后需要改成，真实应用的appid)
    'APLIPAY_APP_NOTIFY_URL': None,  # 应用回调地址[支付成功以后,支付宝返回结果到哪一个地址下面] 一般这里不写，用下面的回调网址即可
    'ALIPAY_DEBUG': False,
    # APIPAY_GATEWAY="https://openapi.alipay.com/gateway.do"   # 真实网关
    'APIPAY_GATEWAY': "https://openapi.alipaydev.com/gateway.do",  # 沙盒环境的网关(上线需要进行修改)
    'ALIPAY_RETURN_URL': "http://127.0.0.1:5000/alipay/result/",  # 同步回调网址--用于前端,支付成功之后回调
    'ALIPAY_NOTIFY_URL': "http://127.0.0.1:5000/pay/result/",  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容，付成功之后回调
    'APP_PRIVATE_KEY_STRING': os.path.join(BASE_DIR, 'server/keys/private_key'),  # 自己生成的私钥，这个就是路径拼接，配置好了，试试能不能点进去
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,********
    'ALIPAY_PUBLIC_KEY_STRING': os.path.join(BASE_DIR, 'server/keys/public_alipay_key'),  # 支付宝给你的公钥
    'SIGN_TYPE': "RSA2",  # RSA 或者 RSA2  现在基本上都是用RSA2
}