# -*- coding: utf-8 -*-
# @Description :
# @File : models.py
# @Time : 2023/3/13 0:50
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


import os
from datetime import datetime

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from server.extensions import db

# Relation Table
# Cart
cart_table = db.Table('cart',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('seat_id', db.Integer, db.ForeignKey('seat.id')),
                db.Column('etc_id', db.Integer),    # 不确定要不要连外键，再说
                db.Column('select_status', db.Boolean, default=False),
                db.Column('create_timestamp', db.DateTime, default=datetime.utcnow),
                db.Column('update_timestamp', db.DateTime)
                )

# class Cart(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     etc_id = db.Column(db.Integer, db.ForeignKey('etc.id'))
#     seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))
#     select_status = db.Column(db.Integer)
#     create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     update_timestamp = db.Column(db.DateTime)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_number = db.Column(db.String(30), db.ForeignKey('order.order_number'))
    etc_id = db.Column(db.Integer, db.ForeignKey('etc.id'))
    etc_name = db.Column(db.String(30))
    begin_timestamp = db.Column(db.DateTime)
    end_timestamp = db.Column(db.DateTime)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))
    seat_name = db.Column(db.String(30))
    seat_type = db.Column(db.Integer)
    price = db.Column(db.Integer)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(128))
    type = db.Column(db.Integer, default=0)     # 是否为管理员，0：不是管理员，1：是管理员
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)
    delete_timestamp = db.Column(db.DateTime)

    orders = db.relationship("Order", back_populates="user")
    seats = db.relationship("Seat", secondary=cart_table, back_populates="users")

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)
        print(self.password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.type == 1


class Etc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String(120))
    begin_timestamp = db.Column(db.DateTime)
    end_timestamp = db.Column(db.DateTime)
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime)

    # relationship
    #   back_populates 双向关系
    #   secondary
    seats = db.relationship("Seat", back_populates="etc")
    medias = db.relationship("Media", back_populates="etc")
    ticket = db.relationship('Ticket', uselist=False)


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    type = db.Column(db.String(30))
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)

    etc_id = db.Column(db.Integer, db.ForeignKey('etc.id'))
    etc = db.relationship('Etc', back_populates="seats")
    ticket = db.relationship('Ticket', uselist=False)

    users = db.relationship("User", secondary=cart_table, back_populates="seats")


class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    type = db.Column(db.Integer)
    url = db.Column(db.String(120))
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime)

    etc_id = db.Column(db.Integer, db.ForeignKey('etc.id'))
    etc = db.relationship('Etc', back_populates="medias")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(30))
    total = db.Column(db.Integer)
    status = db.Column(db.Integer)
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates="orders")
    ticket = db.relationship('Ticket', uselist=False)
