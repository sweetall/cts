# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime


@csrf_exempt
def upload_image(request, dir_name):
    result = {'error': 1, 'message': '上传出错'}
    files = request.FILES.get('imgFile', None)
    if files:
        allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
        file_suffix = files.name.split('.')[-1]
        if file_suffix.lower() not in allow_suffix:
            result = {'error': 1, 'message': '图片格式不正确'}
        else:
            relative_path_file = dir_name + '/%d/%d/' % (datetime.datetime.today().year, datetime.datetime.today().month)
            path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
            if not os.path.exists(path):
                os.makedirs(path)
            file_name = str(uuid.uuid1()) + '.' + file_suffix
            path_file = os.path.join(path, file_name)
            file_url = settings.MEDIA_URL + relative_path_file + file_name
            open(path_file, 'wb').write(files.file.read())
            result = {'error': 0, 'url': file_url}
    return HttpResponse(json.dumps(result), content_type='application/json')


# def upload_file(request, dir_name):
#     result = {'error': 1, 'message': '上传出错'}
#     files = request.FILES.get('file_field', None)
#     if files:
#         file_suffix = files.name.split('.')[-1]
#         relative_path_file = 'files/%d/%d/' % (datetime.datetime.today().year, datetime.datetime.today().month)
#         path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
#         if not os.path.exists(path):
#             os.makedirs(path)
#         file_name = str(uuid.uuid1()) + '.' + file_suffix
#         path_file = os.path.join(path, file_name)
#         file_url = settings.MEDIA_URL + relative_path_file + file_name
#         open(path_file, 'wb').write(files.file.read())
#         result = {'error': 0, 'url': file_url}
#     return HttpResponse(json.dumps(result), content_type='application/json')
