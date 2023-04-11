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


class Bullet(db.Model):
    __tablename__ = 'bullet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    etc_id = db.Column(db.Integer, db.ForeignKey('etc.id'))
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    msg = db.Column(db.String(255))

    user = db.relationship('User', back_populates='user_etcs')
    etc = db.relationship('Etc', back_populates='etc_users')


class Cart(db.Model):
    __tablename__ = 'cart'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # etc_id = db.Column(db.Integer, db.ForeignKey('etc.id'), primary_key=True)
    etc_id = db.Column(db.Integer)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), primary_key=True)
    select_status = db.Column(db.Integer, default=0)
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='user_seats')
    seat = db.relationship('Seat', back_populates='seat_users')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    password = db.Column(db.String(128))
    type = db.Column(db.Integer, default=0)     # 是否为管理员，0：不是管理员，1：是管理员
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    deleted = db.Column(db.Boolean, default=False)
    delete_timestamp = db.Column(db.DateTime)

    orders = db.relationship("Order", back_populates="user")    # one-to-many
    user_seats = db.relationship("Cart", back_populates="user")  # many-to-many
    user_etcs = db.relationship("Bullet", back_populates="user")  # many-to-many

    def get_id(self):
        return self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)
        # print(self.password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def delete(self):
        self.deleted = 1
        self.delete_timestamp = datetime.now()
        return self.delete_timestamp

    @property
    def is_admin(self):
        return self.type == 1

    @property
    def is_deleted(self):
        return self.deleted == 1


class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    type = db.Column(db.String(30))
    create_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    update_timestamp = db.Column(db.DateTime)
    price = db.Column(db.Integer)
    status = db.Column(db.Integer, default=0)

    etc_id = db.Column(db.Integer, db.ForeignKey('etc.id'))  # many
    etc = db.relationship('Etc', back_populates="seats")
    ticket = db.relationship('Ticket', uselist=False)

    seat_users = db.relationship("Cart", back_populates="seat")   # many-to-many


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
    seats = db.relationship("Seat", back_populates="etc")
    medias = db.relationship("Media", back_populates="etc")
    ticket = db.relationship('Ticket', uselist=False)
    etc_users = db.relationship("Bullet", back_populates="etc")  # many-to-many

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

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))   # many-to-one
    user = db.relationship('User', back_populates="orders")     # many-to-one
    ticket = db.relationship('Ticket', uselist=False)


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
