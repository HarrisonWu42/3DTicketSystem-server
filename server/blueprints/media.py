# -*- coding: utf-8 -*-
# @Description :
# @File : media.py
# @Time : 2023/4/9 19:35
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from math import ceil
from flask import Blueprint, jsonify
from server.extensions import db
from server.models import Media, Etc
from server.utils import medias2json


media_bp = Blueprint('media', __name__)


@media_bp.route('/query_medias/<etc_id>/<offset>/<page_size>', methods=['GET'])
def query_media_list(etc_id, offset, page_size):
    etc_id = int(etc_id)
    page_size = int(page_size)
    offset = int(offset)

    etc = Etc.query.filter_by(etc_id=etc_id).first()
    if etc is None:
        return jsonify(code=401, message='Etc not exist.')

    medias = Media.query.filter_by(deleted=0).all()
    page_users = medias[(offset - 1) * page_size: offset * page_size]
    total_pages = ceil(len(medias) / page_size)
    data = medias2json(page_users)
    data['total_pages'] = total_pages
    data['user_num'] = len(page_users)

    return jsonify(code=200, data=data)