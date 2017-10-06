# -*- coding: utf-8 -*-
"""
Modèles de l'application.
"""

from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class Station(models.Model):
    """
    Décrit une gare avec son nom et ses coordonnées GPS.
    """
    name = models.CharField(max_length=40)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name


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


class Train(models.Model):
    """
    Décrit un train, avec son numéro et sa période de service.
    """
    number = models.PositiveIntegerField()
    period = models.ForeignKey('Period', on_delete=models.PROTECT)
    traintype = models.ForeignKey('TrainType', on_delete=models.PROTECT)


class TrainType(models.Model):
    """
    Décrit un type de train.
    """
    name = models.CharField(max_length=20)
    icon = models.FilePathField(path=settings.BASE_DIR+'/main/static/main/img')


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
