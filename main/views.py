# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm, SignUpForm
from .models import Travel


def search(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        # TODO: Rediriger vers la vue de résultats
        pass
    return render(request, 'main/search.html', dict(active="search"))


def searchResult(request):
    return render(request, 'main/searchResult.html', dict(active="search"))


def tickets(request):
    return render(request, 'main/tickets.html', dict(active="list"))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/train/')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})


def print_ticket(request, travel_id):
    """Vue permettant l'impression d'un ensemble de billets."""
    if not request.user.is_authenticated():
        return redirect('search')
    return render(request, 'main/print.html',
                  {'travel': get_object_or_404(Travel, id=travel_id)})
