# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from django.template import RequestContext


def handler400(request):
    response = render_to_response('main/errors/400.html')
    response.status_code = 400
    return response


def handler403(request):
    response = render_to_response('main/errors/403.html')
    response.status_code = 403
    return response


def handler404(request):
    response = render_to_response('main/errors/404.html')
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('main/errors/500.html')
    response.status_code = 500
    return response
