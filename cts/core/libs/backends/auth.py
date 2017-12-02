# -*- coding: utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class APILogin(ModelBackend):
    """
    API auth backend
    """
    def authenticate(self, username=None, password=None, chinese_name=None, email=None, phone=None, **kwargs):
        """
        Get or create user
        """
        update_defaults = {}
        if email:
            update_defaults['email'] = email
        user, created = User.objects.update_or_create(username=username, defaults=update_defaults)

        if phone:
            user.userprofile.phone = phone
        if chinese_name:
            user.userprofile.chinese_name = chinese_name
        user.userprofile.save()

        user.set_password(password)
        user.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None