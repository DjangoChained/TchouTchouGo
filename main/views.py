# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def search(request):
    return render(request, 'main/search.html', dict(active="search"))
