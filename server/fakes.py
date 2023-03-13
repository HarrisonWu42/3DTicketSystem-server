# -*- coding: utf-8 -*-
# @Description :
# @File : fakes.py
# @Time : 2023/3/13 0:56
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


import random
import datetime
from faker import Faker
from sqlalchemy.exc import IntegrityError

import server
from server.extensions import db
from server.models import User, Etc, Seat, Media, Order, Ticket

fake = Faker(locale='en_US')


def db_init():
    server.db.create_all()


# fake_user(10)


def fake_user(count=10):
    user_admin = User(name='admin', type=1)
    user_admin.set_password('123456')
    db.session.add(user_admin)
    db.session.commit()

    for i in range(count):
        user = User(name=fake.name())
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            print(IntegrityError)
            db.session.rollback()


def fake_etc(count=10):
    for i in range(count):
        begin_timestamp = fake.date_time()
        end_timestamp = begin_timestamp+datetime.timedelta(minutes=random.randint(60, 180))
        etc = Etc(name='etc' + fake.postcode(),
                  begin_timestamp=begin_timestamp,
                  end_timestamp=end_timestamp)
        db.session.add(etc)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_seat(count=10):
    for i in range(count):
        seat = Seat(name='seat' + fake.postcode(),
                   price=180)
        db.session.add(seat)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()