#!/usr/bin/python
# -*- encoding=utf-8 -*-

from django.shortcuts import render

def api_documents(request):
    """

    :param request:
    :return:
    """
    return render(
        request=request,
        template_name='index.html'
    )
