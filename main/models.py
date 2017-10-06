# -*- coding: utf-8 -*-
"""
Modèles de l'application.
"""

from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from .utility import haversine


class Station(models.Model):
    """
    Décrit une gare avec son nom et ses coordonnées GPS.
    """
    name = models.CharField(max_length=40)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name

    @property
    def coords(self):
        return (self.lat, self.lng)

    @coords.setter
    def set_coords(self, value):
        self.lat = value[0]
        self.lng = value[1]

    def distance_to(self, station):
        return haversine(self.lon, self.lat, station.lon, station.lat)


class Halt(models.Model):
    """
    Décrit l'arrêt d'un train en gare, avec les heures d'arrivée et de départ,
    et le numéro de séquence de l'arrêt (ordre dans lequel le train passe),
    ainsi que le train et la gare concernés.
    """
    arrival = models.TimeField()
    departure = models.TimeField()
    sequence = models.PositiveSmallIntegerField()
    train = models.ForeignKey('Train', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.PROTECT)

    def __str__(self):
        return "Arrêt du " + str(self.train) + " à " + str(self.station)


class Train(models.Model):
    """
    Décrit un train, avec son numéro et sa période de service.
    """
    number = models.PositiveIntegerField()
    period = models.ForeignKey('Period', on_delete=models.PROTECT)
    traintype = models.ForeignKey('TrainType', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.traintype) + str(self.number)


class TrainType(models.Model):
    """
    Décrit un type de train.
    """
    name = models.CharField(max_length=20)
    icon = models.FilePathField(path=settings.BASE_DIR+'/main/static/main/img')
    km_price = models.FloatField(default=1.0)

    def __str__(self):
        return self.name


class Period(models.Model):
    """
    Décrit une période de service.
    Une période de service décrit les jours de la semaine, durant un intervalle
    de dates donnés, durant lesquelles un train circule.
    Les champs de monday à sunday sont des booléens indiquant si le train
    circule durant ce jour de la semaine.
    start_date et end_date décrivent la période de validité de ce service.
    Par exemple, pour un train circulant du lundi au vendredi durant toute
    l'année 2018, les champs vaudront :
    True True True True True False False 01/01/2018 31/12/2018
    """
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return "Service entre " + str(self.start_date) + " et " + \
            str(self.end_date)


class PeriodException(models.Model):
    """
    Décrit une exception de période de service.
    Les exceptions de période de service sont des jours durant lesquels un
    train peut circuler en plus ou ne pas circuler du tout.
    Une période de service avec des exceptions pourrait être décrite ainsi :
    "Ce train circule du lundi au vendredi durant toute l'année 2018,
    sauf le 1er mai où il ne circulera pas et sauf le 4 août (un samedi)
    où il circulera exceptionnellement."
    Dans ce cas, il y a deux PeriodExceptions :
    (01/05/2018, True) et (04/08/2018, False).
    add_day vaut True si le train circulera, False s'il ne circule pas.
    Dans GTFS, add_day correspond à exception_type et vaut 1 si le train
    circule et 2 s'il ne circule pas.
    """
    date = models.DateField()
    add_day = models.BooleanField()
    period = models.ForeignKey('Period', on_delete=models.CASCADE)
    unique_together = ("date", "period")

    def __str__(self):
        return "Exception pour le " + str(self.period) + \
            ", le " + str(self.date)


class Ticket(models.Model):
    """
    Décrit un billet de train. Un billet représente un voyage dans un seul
    train, d'un arrêt à un autre.
    """
    sequence = models.PositiveSmallIntegerField()
    start_halt = models.ForeignKey('Halt', on_delete=models.PROTECT,
                                   related_name='+')
    end_halt = models.ForeignKey('Halt', on_delete=models.PROTECT,
                                 related_name='+')
    travel = models.ForeignKey('Travel', on_delete=models.CASCADE)

    @property
    def distance(self):
        """Distance parcourue en kilomètres."""
        return self.start_halt.station.distance_to(self.end_halt.station)

    @property
    def price(self):
        """Prix du billet."""
        return self.distance * self.start_halt.train.traintype.km_price


class Travel(models.Model):
    """
    Décrit un voyage. Un voyage peut contenir plusieurs billets, qui feront
    une correspondance.
    """
    date = models.DateField()
    passengers = models.PositiveSmallIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def start_station(self):
        """Station de départ du voyage."""
        return self.ticket_set.get(sequence=0).start_halt.station

    @property
    def end_station(self):
        """Station d'arrivée du voyage."""
        return self.ticket_set.order_by('-sequence')[:1].station

    @property
    def start_time(self):
        """Heure de départ du voyage."""
        return self.ticket_set.get(sequence=0).start_halt.departure

    @property
    def end_time(self):
        """Heure d'arrivée du voyage."""
        return self.ticket_set.order_by('-seqeunce')[:1].arrival

    @property
    def total_price(self):
        """Prix total du voyage."""
        return sum([t.price for t in self.ticket_set.all()]) * self.passengers

    @property
    def total_distance(self):
        """Distance totale du voyage."""
        return sum([t.distance for t in self.ticket_set.all()])
