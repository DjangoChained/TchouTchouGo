# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SearchForm, SignUpForm, UserForm
from .models import Travel, Station

from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


def search(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        # TODO: Rediriger vers la vue de résultats
        pass
    stations = Station.objects.all()
    return render(request, 'main/search.html', dict(
        active="search", stations=stations))


def searchResult(request):
    return render(request, 'main/searchResult.html', dict(
        active="search",
        travels=request.user.travel_set.all))


def tickets(request):
    if not request.user.is_authenticated():
        return redirect('search')
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


@login_required()
def update_profile(request):
    user = User.objects.get(pk=request.user.id)
    # prepopulate UserProfileForm with retrieved user values from above.
    form = UserForm(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            form = UserForm(request.POST, request.FILES, instance=user)

            if form.is_valid():
                created_user = form.save(commit=False)
                created_user.save()
                return redirect('/train/updateProfile')
        return render(request, "registration/updateProfile.html", {
            'form': form
        })
    else:
        raise PermissionDenied
