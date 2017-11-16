# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .forms import SearchForm, SignUpForm, UserForm, PassengerForm
from django.forms.models import model_to_dict
from .models import Travel, Station, Passenger
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
import json


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
                         request.POST.getlist('passengers'),
                         TimeOptions[form.cleaned_data.get('timeOptions')])))
    passengers = ""
    if request.user.is_authenticated():
        passengers = request.user.passenger_set.filter(display=True)
    #Stations pour l'autocomplétion des gares
    stations = Station.objects.all()
    res = [{'id': s.id, 'label': s.name, 'value': s.name} for s in stations]
    return render(request, 'main/search.html',
                  dict(active="search", passengers=passengers,
                       stations=json.dumps(res),
                       hours=range(5, 23)))


@login_required
def tickets(request):
    return render(request, 'main/tickets.html',
                  dict(active="list",
                       travel_set=Travel.objects.filter(booked=True)))


def basket(request):
    if not request.user.is_authenticated():
        return redirect('search')
    return render(request, 'main/basket.html', dict(active="basket"))


@login_required
def passengers(request):
    passengers = request.user.passenger_set.filter(display=True)
    return render(request, 'main/passengers.html', dict(passengers=passengers))


@login_required
def addPassenger(request):
    form = PassengerForm()

    if request.method == "POST":
        form = PassengerForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('passengers')
    else:
        form = PassengerForm()

    return render(request, 'main/addPassenger.html', {'form': form})


@login_required
def updatePassenger(request, passenger_id):
    passenger = Passenger.objects.get(id=passenger_id)
    # On remplit PassengerForm avec les données de l'utilisateur récupérées

    form = PassengerForm(request.POST or None, instance=passenger)

    if request.method == "POST":
        edit = False
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('passengers')
    else:
        edit = True

    return render(request, 'main/addPassenger.html',
                  {'form': form, 'last_name': passenger.last_name,
                   'first_name': passenger.first_name, 'edit': edit})


@login_required
def deletePassenger(request, passenger_id):
    passenger = request.user.passenger_set.filter(display=True) \
        .get(id=passenger_id)
    #l'utilisateur doit toujours avoir au moins 1 passager
    if passenger.user.passenger_set.filter(display=True).count() > 1:
        #Si le passager est associé à des voyages, on ne le supprime pas,
        #on se contente de ne plus l'afficher à l'utilisateur
        if passenger.travel_set.count() > 0:
            passenger.display = False
            passenger.save()
        #Sinon on peut le supprimer
        else:
            passenger.delete()
    return redirect('/train/passengers')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            passenger = Passenger(
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'))
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/train/')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})


@login_required
def print_ticket(request, travel_id):
    """Vue permettant l'impression d'un ensemble de billets."""
    travel = get_object_or_404(Travel, id=travel_id)
    if not travel.booked:
        return HttpResponseBadRequest()
    return render(request, 'main/print.html',
                  {'travel': travel})


@login_required
def update_profile(request):
    user = User.objects.get(pk=request.user.id)
    # On remplit UserProfileForm avec les données de l'utilisateur récupéré
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
