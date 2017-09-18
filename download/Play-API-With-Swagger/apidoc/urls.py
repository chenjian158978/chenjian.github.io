#!/usr/bin/python
# -*- encoding=utf-8 -*-

from django.conf.urls import url
from qgsprocessor2017.apps.apidoc.views import api_documents

urlpatterns = [
    url(r'^$', api_documents),
]
