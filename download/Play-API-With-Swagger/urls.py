#!/usr/bin/python
# -*- encoding=utf-8 -*-

from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/doc/', include("mouprojects.apps.apidoc.urls")),
]
