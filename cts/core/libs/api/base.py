# -*- coding: utf-8 -*-
import os
import requests
import logging


from django.conf import settings

logger = logging.getLogger('application')


def auth(token):
    payload = {'key': token}
    try:
        r = requests.post(settings.LOPS_AUTH_API, data=payload)
        print settings.LOPS_AUTH_API
        data = r.json()
        user_info = {}
        if data['status']:
            user_info.update({
                'username': data['data']['username'],
                'email': '%s@pingan.com.cn' % data['data']['username']
            })
            return True, user_info
        return False, False
    except Exception as err:
        print err
        logger.error(err, exc_info=True)
        return False, False


def send_mail(subject, to, message='', html=None, cc=None):
    payload = {
        'subject': subject,
        'message': message,
        'to': to,
        'cc': cc,
        'html': html
    }
    try:
        r = requests.post(settings.LOPS_EMAIL_API, data=payload)
        data = r.json()
        if data['status']:
            return 'Send email successfully'
        else:
            return data['message']
    except Exception as err:
        logger.error(err, exc_info=True)
        return str(err)
