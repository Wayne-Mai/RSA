"""Django URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

import project.views

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^$', project.views.home),
    url(r'^hello', project.views.contact_gen_key),
    url(r'^genkey', project.views.contact_gen_key),
    url(r'^encoder', project.views.encode_contact),
    url(r'^decoder', project.views.decode_contact),
    #pictures

    ]

urlpatterns=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+urlpatterns
