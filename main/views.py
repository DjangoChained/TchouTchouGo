# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .forms import SearchForm, SignUpForm, UserForm, PassengerForm
from .models import Travel, Station, Passenger
from .search import TimeOptions, search as search_trains

from datetime import time
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import \
    render, redirect, get_object_or_404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest
import json
import geojson
from easycart import BaseCart


def search(request):
    passengers = []
    if request.user.is_authenticated():
        passengers = request.user.passenger_set.filter(display=True).all()
    if request.method == 'POST':
        form = SearchForm(request.POST, passengers=passengers)
        if form.is_valid():
            start_station = Station.objects.get(
                name=form.cleaned_data.get('startStation'))
            end_station = Station.objects.get(
                name=form.cleaned_data.get('endStation'))
            ps = []
            if 'passengers' in dict(request.POST.lists()):
                ps = [passengers.get(id=id)
                      for id in dict(request.POST.lists())['passengers']]
            return render(
                request, 'main/searchResult.html',
                dict(active="search",
                     start_station=start_station,
                     end_station=end_station,
                     results=search_trains(
                         start_station, end_station,
                         form.cleaned_data.get('travelDate'),
                         time(hour=int(form.cleaned_data.get('hour'))), ps,
                         TimeOptions[form.cleaned_data.get('timeOptions')])))
    passengers = ""
    if request.user.is_authenticated():
        passengers = request.user.passenger_set.filter(display=True)
    return render(request, 'main/search.html', dict(
        active="search", passengers=passengers, hours=range(5, 23)))


@login_required
def tickets(request):
    return render(request, 'main/tickets.html', dict(
        active="list", travel_set=Travel.objects.filter(
            booked=True, passengers_aboard__user=request.user).distinct()))


###############################################################################
# Gestion du panier
###############################################################################


class Cart(BaseCart):
    """Décrit le panier de billets."""
    ## Quantité maximale de chaque voyage.
    # Doit être défini à 1, car il n'est pas question de commander plusieurs
    # fois un voyage avec un même identifiant, contrairement à un panier de
    # magasin en ligne par exemple.
    max_quantity = 1

    def get_queryset(self, pks):
        """Obtenir un QuerySet correspondant aux billets pouvant se trouver
        dans le panier."""
        return Travel.objects.filter(booked=False, pk__in=pks)


@login_required
def cart_show(request):
    return render(request, 'main/cart.html', dict(active="cart", total_price=sum(i.price for i in Cart(request).list_items())))


@login_required
def cart_add(request, travel_id):
    Cart(request).add(travel_id)
    return redirect('/train/cart')


@login_required
def cart_remove(request, travel_id):
    Cart(request).remove(travel_id)
    return redirect('/train/cart')


@login_required
def order(request):
    for i in Cart(request).list_items():
        i.obj.booked = True
        i.obj.save()
    return redirect('/train/tickets')


###############################################################################
# Gestion des passagers
###############################################################################


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
            doublon = Passenger.objects.filter(
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                display=False)
            if doublon.count():
                Passenger.objects.select_for_update() \
                    .filter(id=doublon.first().id).update(display=True)
            else:
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
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            Passenger.objects.create(
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                user=request.user)
            return redirect('/train/')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})


###############################################################################
# Cartographie
###############################################################################


def full_map(request):
    from TchouTchouGo.settings import GOOGLE_MAPS_API_KEY
    return render(request, 'main/map.html', {
        'active': 'map',
        'api_key': GOOGLE_MAPS_API_KEY})


def full_map_geojson(request):
    points = geojson.FeatureCollection([
        geojson.Feature(geometry=geojson.Point((s.lng, s.lat)),
                        properties={"title": s.name})
        for s in Station.objects.all()])
    return HttpResponse(geojson.dumps(points), content_type='application/json')


def travel_map(request, travel_id):
    from TchouTchouGo.settings import GOOGLE_MAPS_API_KEY
    return render(request, 'main/travel_map.html', {
        'travel_id': travel_id,
        'api_key': GOOGLE_MAPS_API_KEY})


def travel_map_geojson(request, travel_id):
    from django.db.models import Q
    tr = get_object_or_404(Travel, id=travel_id)
    stations = [t.start_halt.station for t in tr.ticket_set.all()]
    stations.append(tr.ticket_set.reverse()[0].end_halt.station)
    print(stations)
    data = [geojson.Feature(geometry=geojson.Point((s.lng, s.lat)),
                            properties={"title": s.name})
            for s in stations]
    data.append(geojson.Feature(
        geometry=geojson.LineString([(s.lng, s.lat) for s in stations]),
        properties={"strokeColor": "red", "strokeWeight": 3}))
    return HttpResponse(geojson.dumps(geojson.FeatureCollection(data)),
                        content_type="application/json")


###############################################################################
# Fonctionnalités secondaires
###############################################################################


@login_required
def print_ticket(request, travel_id):
    """Vue permettant l'impression d'un ensemble de billets."""
    travel = get_object_or_404(Travel, id=travel_id,
                               passengers_aboard__user=request.user)
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


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/train/search')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/updatePassword.html')


def stations_json(request):
    return HttpResponse(json.dumps(
        [{'id': s.id, 'label': s.name, 'value': s.name}
         for s in Station.objects.all()]), content_type="application/json")
