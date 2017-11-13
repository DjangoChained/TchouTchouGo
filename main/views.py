# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .forms import SearchForm, SignUpForm, UserForm
from .models import Travel, Station
from .search import TimeOptions, search as search_trains

from datetime import time
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import \
    render, redirect, get_object_or_404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            start_station = Station.objects.get(
                name=form.cleaned_data.get('startStation'))
            end_station = Station.objects.get(
                name=form.cleaned_data.get('endStation'))

            return render(
                request, 'main/searchResult.html',
                dict(active="search",
                     start_station=start_station,
                     end_station=end_station,
                     results=search_trains(
                         start_station, end_station,
                         form.cleaned_data.get('travelDate'),
                         time(hour=int(form.cleaned_data.get('hour'))),
                         form.cleaned_data.get('passengers'),
                         TimeOptions[form.cleaned_data.get('timeOptions')])))
    return render(request, 'main/search.html', dict(active="search"))


@login_required()
def tickets(request):
    return render(request, 'main/tickets.html',
                  dict(active="list",
                       travel_set=Travel.objects.filter(booked=False)))


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


@login_required()
def print_ticket(request, travel_id):
    """Vue permettant l'impression d'un ensemble de billets."""
    travel = get_object_or_404(Travel, id=travel_id)
    if not travel.booked:
        return HttpResponseBadRequest()
    return render(request, 'main/print.html',
                  {'travel': travel})


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
