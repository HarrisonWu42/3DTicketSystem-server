# -*- coding: utf-8 -*-
# @Description :
# @File : utils.py
# @Time : 2023/4/9 16:37
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


def users2json(users):
    json_array = []
    for user in users:
        role = 'user'
        if user.is_admin is True:
            role = 'admin'

        user_obj = {'id': user.id,
                    'name': user.name,
                    'role': role,
                    'create_timestamp': user.create_timestamp,
                    'update_timestamp': user.update_timestamp}
        json_array.append(user_obj)
    json_dic = {"users": json_array}

    return json_dic


def medias2json(medias):
    json_array = []
    for media in medias:
        media_obj = {'id': media.id,
                     'name': media.name,
                     'type': media.type,
                     'url': media.url,
                     'etc_id': media.etc_id,
                     'create_timestamp': media.create_timestamp,
                     'update_timestamp': media.update_timestamp}
        json_array.append(media_obj)
    json_dic = {"medias": json_array}

    return json_dic


def seats2json(seats):
    json_array = []
    for seat in seats:
        seat_obj = {'id': seat.id,
                    'name': seat.name,
                    'type': seat.type,
                    'create_timestamp': seat.create_timestamp,
                    'update_timestamp': seat.update_timestamp,
                    'price': seat.price,
                    'status': seat.status,
                    'etc_id': seat.etc_id}
        json_array.append(seat_obj)
    json_dic = {"seats": json_array}

    return json_dic