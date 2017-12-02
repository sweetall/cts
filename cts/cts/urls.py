"""cts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from blog import urls as blog_urls
from core import urls as core_urls
from core.page_views import login, logout
from core.libs.auth.decorators import login_required
from core.libs.upload import upload_image
from core.libs.utils.urls import required
from blog.page_views import index

urlpatterns = [
    url(r'^cts/admin/', admin.site.urls),
    # url(r'^$', IndexView.as_view(), name='index'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^cts/login/$', login, name='login'),
    url(r'^cts/logout/$', logout, name='logout'),
]

urlpatterns += required(login_required, [
    url(r'^cts/$', index, name='index'),
    url(r'^cts/core/', include(core_urls, namespace='core')),
    url(r'^cts/blog/', include(blog_urls, namespace='blog')),

    url(r'^cts/upload_image/(?P<dir_name>[^/]+)$', upload_image, name='upload_image')
])
