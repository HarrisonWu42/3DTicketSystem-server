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