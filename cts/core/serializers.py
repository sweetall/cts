# -*- coding: utf-8 -*-
from rest_framework import serializers

from models import *


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(source='user.username')
    messages = serializers.StringRelatedField(source='user.messages', many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

