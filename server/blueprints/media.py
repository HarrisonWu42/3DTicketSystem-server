# -*- coding: utf-8 -*-
# @Description :
# @File : media.py
# @Time : 2023/4/9 19:35
# @Author : HarrisonWu42
# @Email: harrisonwu.com@gmail.com
# @Software: PyCharm


from math import ceil
from flask import Blueprint, jsonify, request
from server.extensions import db
from server.models import Media, Etc
from server.utils import medias2json, AliyunOss


media_bp = Blueprint('media', __name__)


@media_bp.route('/query_medias/<etc_id>/<offset>/<page_size>', methods=['GET'])
def query_media_list(etc_id, offset, page_size):
    etc_id = int(etc_id)
    page_size = int(page_size)
    offset = int(offset)

    etc = Etc.query.filter_by(id=etc_id).first()
    if etc is None:
        return jsonify(code=401, message='Etc not exist.')

    medias = etc.medias
    page_medias = medias[(offset - 1) * page_size: offset * page_size]
    total_pages = ceil(len(medias) / page_size)
    data = medias2json(page_medias)
    data['total_pages'] = total_pages
    data['media_num'] = len(page_medias)

    return jsonify(code=200, data=data)


@media_bp.route('/upload', methods=['POST'])
def upload():
    name = request.form['name']
    type = request.form['type']
    etc_id = int(request.form['etc_id'])
    filepath = request.form['filepath']

    etc = Etc.query.get(etc_id)
    if etc is None:
        return jsonify(code=403, message="Etc not exist.")
    # # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。这里用的是RAM子用户的AccessKey，课程结束记得关掉
    # auth = oss2.Auth('LTAI5t8pHVm8Xn7TZyDXCqJN', 'xeDexfxUApQ8rw1IyFKTQE0ojmBlSC')  # <yourAccessKeyId> <yourAccessKeySecret>
    # bucket = oss2.Bucket(auth, 'http://oss-cn-guangzhou.aliyuncs.com', 'software-3dticket42')  # <Endpoint> <yourBucketName>

    # 上传文件到OSS。
    # <yourObjectName>由包含文件后缀，不包含Bucket名称组成的Object完整路径，例如abc/efg/123.jpg。
    # <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
    # bucket.put_object_from_file(name, filepath)  # '<yourObjectName>', '<yourLocalFile>'

    object_name = "test/" + name
    url = AliyunOss().put_object_from_file(object_name, filepath)

    media = Media(name=name, type=type, url=url, etc_id=etc_id)
    db.session.add(media)
    db.session.commit()

    return jsonify(code=200, data={"id": media.id,
                                   "name": media.name,
                                   "type": media.type,
                                   "url": url,
                                   "etc_id": media.etc_id,
                                   "create_timestamp": media.create_timestamp,
                                   "update_timestamp": media.update_timestamp})
