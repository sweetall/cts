# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import resolve_url, get_object_or_404
from django.utils.http import is_safe_url
from django.contrib.auth import logout as auth_logout, login as auth_login, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.admin.options import get_content_type_for_model
from django.utils.encoding import force_text
from django.contrib import messages

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(AuthenticationForm):
    """
    Login Form
    """

    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(request=request, *args, **kwargs)
        self.request = request
        self.helper = FormHelper()
        self.helper.add_input(Submit('signin', '登陆', css_class='btn-flat right-side'))


def login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Login view
    :param request: 
    :param redirect_field_name: 
    :return: 
    """
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

    form = LoginForm(request=request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            auth_login(request, form.get_user())

            return redirect(redirect_to)
    return render(request, 'core/login.html', {'form': form})


def logout(request):
    """
    Logout view
    :param request: 
    :return: 
    """
    auth_logout(request)
    response = redirect(settings.LOGIN_URL)
    if settings.LOGIN_URL == '/login/':
        response.set_cookie(settings.LOPS_AUTH_COOKIE, '')
    return response
