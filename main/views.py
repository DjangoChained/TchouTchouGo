# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .forms import SearchForm


def search(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        # TODO: Rediriger vers la vue de résultats
        pass
    return render(request, 'main/search.html', dict(active="search"))
