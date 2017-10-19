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
    ## Nom de la gare.
    name = models.CharField(max_length=40)
    ## Composante de latitude des coordonnées GPS de la gare.
    lat = models.FloatField()
    ## Composante de longitude des coordonnées GPS de la gare.
    lng = models.FloatField()

    class Meta:
        """Métadonnées du modèle de station."""
        ## Nom affiché dans l'interface d'administration Django.
        verbose_name = "gare"

    def __str__(self):
        """Représentation textuelle de la gare pour affichage."""
        return self.name

    @property
    def coords(self):
        """Obtenir un tuple (latitude, longitude) correspondant aux
        coordonnées GPS de la gare."""
        return (self.lat, self.lng)

    @coords.setter
    def set_coords(self, value):
        """Définir les coordonnées GPS de la gare à l'aide d'un tuple
        (latitude, longitude)."""
        self.lat = value[0]
        self.lng = value[1]

    def distance_to(self, station):
        """Calculer la distance depuis cette gare vers une autre gare,
        à vol d'oiseau."""
        return haversine(self.lng, self.lat, station.lng, station.lat)


class Halt(models.Model):
    """
    Décrit l'arrêt d'un train en gare, avec les heures d'arrivée et de départ,
    et le numéro de séquence de l'arrêt (ordre dans lequel le train passe),
    ainsi que le train et la gare concernés.
    """
    ## Heure d'arrivée du train en gare.
    arrival = models.TimeField()
    ## Heure de départ du train depuis la gare.
    departure = models.TimeField()
    ## Numéro de séquence de l'arrêt. Base 0.
    #  Permet d'ordonner les arrêts pour un train.
    sequence = models.PositiveSmallIntegerField()
    ## Association avec un train.
    #  La suppression d'un train entraîne la suppression de ses arrêts.
    train = models.ForeignKey('Train', null=True, on_delete=models.CASCADE)
    ## Association avec une gare.
    #  Il est impossible de supprimer une gare s'il existe un train s'y
    #  arrêtant.
    station = models.ForeignKey('Station', null=True, on_delete=models.PROTECT)

    class Meta:
        """Métadonnées du modèle d'arrêt de train en gare."""
        ## Ordre utilisé par défaut quand aucune clause order_by() n'est
        #  spécifiée dans un QuerySet.
        ordering = ["train", "sequence"]
        ## Index de type unique assurant qu'il n'y ait pas deux arrêts avec la
        #  même position dans l'itinéraire.
        unique_together = ("train", "sequence")
        ## Nom affiché dans l'interface d'administration de Django.
        verbose_name = "arrêt d'un train en gare"
        ## Nom affiché au pluriel dans l'administration de Django.
        verbose_name_plural = "arrêts des trains en gares"

    def __str__(self):
        """Représentation textuelle de l'arrêt"""
        return "Arrêt du " + str(self.train) + " à " + str(self.station)


class Train(models.Model):
    """
    Décrit un train, avec son numéro et sa période de service.
    """
    ## Numéro du train.
    #  Le numéro donné par la SNCF n'est pas unique ; il est seulement affiché
    #  pour faciliter sa reconnaissance par les utilisateurs, le format GTFS
    #  oblige la SNCF à faire de la redondance sur ce numéro.
    number = models.PositiveIntegerField()
    ## Association avec une période de service.
    #  Si un train utilise une période, on ne peut pas la supprimer.
    period = models.ForeignKey('Period', null=True, on_delete=models.PROTECT)
    ## Association avec un type de train.
    #  Si un train utilise un type de train, on ne peut pas le supprimer.
    traintype = models.ForeignKey('TrainType', on_delete=models.PROTECT)

    class Meta:
        """Métadonnées du modèle de train."""
        ## Nom affiché dans l'interface d'administration de Django.
        verbose_name = "train"

    def __str__(self):
        """Représentation textuelle du train pour l'affichage."""
        return str(self.traintype) + " " + str(self.number)


class TrainType(models.Model):
    """
    Décrit un type de train.
    """
    ## Nom affiché du type de train.
    name = models.CharField(max_length=20)
    ## Prix kilométrique pour ce type de train.
    #  Permet de simuler un calcul des prix à l'aide des distances entre
    #  stations.
    km_price = models.FloatField(default=1.0)

    class Meta:
        """Métadonnées du modèle de type de train."""
        ## Nom affich dans l'interface d'administration de Django.
        verbose_name = "type de train"

    def __str__(self):
        """Représentation textuelle du type de train pour l'affichage."""
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
    ## Indique si les trains circulent le lundi.
    monday = models.BooleanField()
    ## Indique si les trains circulent le mardi.
    tuesday = models.BooleanField()
    ## Indique si les trains circulent le mercredi.
    wednesday = models.BooleanField()
    ## Indique si les trains circulent le jeudi.
    thursday = models.BooleanField()
    ## Indique si les trains circulent le vendredi.
    friday = models.BooleanField()
    ## Indique si les trains circulent le samedi.
    saturday = models.BooleanField()
    ## Indique si les trains circulent le dimanche.
    sunday = models.BooleanField()
    ## Indique la date de début de validité de la période.
    start_date = models.DateTimeField()
    ## Indique la date de fin de validité de la période.
    end_date = models.DateTimeField()

    class Meta:
        """Métadonnées du modèle de période de service."""
        ## Nom affiché dans l'interface d'administration de Django.
        verbose_name = "période de service"
        ## Nom au pluriel affiché dans l'administration de Django.
        verbose_name_plural = "périodes de service"

    def __str__(self):
        """Représentation textuelle de la période pour l'affichage."""
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
    ## Date de l'exception
    date = models.DateField()
    ## Indique si c'est un jour supplémentaire ou un jour supprimé.
    #  Vaut True si le train circulera ce jour-là, False sinon.
    add_day = models.BooleanField()
    ## Association avec une période de service.
    #  Les exceptions sont automatiquement supprimées quand une période
    #  de service est supprimée.
    period = models.ForeignKey('Period', on_delete=models.CASCADE)

    class Meta:
        """Métadonnées du modèle d'exception de période de service."""
        ## Tri par défaut des exceptions par période.
        ordering = ["period"]
        ## Nom affiché dans l'interface d'administration de Django.
        verbose_name = "exception à une période de service"
        ## Nom au pluriel affiché dans l'administration de Django.
        verbose_name_plural = "exceptions à une période de service"
        ## Contrainte d'unicité assurant qu'il n'y ait pas plusieurs
        #  exceptions pour la même date dans la même période.
        unique_together = ("date", "period")

    def __str__(self):
        """Représentation textuelle de l'exception pour affichage."""
        return u"Exception pour le " + str(self.period) + \
            ", le " + str(self.date)


class Ticket(models.Model):
    """
    Décrit un billet de train. Un billet représente un voyage dans un seul
    train, d'un arrêt à un autre.
    """
    ## Numéro de séquence du billet dans un voyage. Base zéro.
    #  Permet d'ordonner les billets dans un voyage donné.
    sequence = models.PositiveSmallIntegerField()
    ## Arrêt de départ. Ce n'est pas une station ou un train puisqu'il est
    #  tout à fait possible de monter dans un train à une gare intermédiaire.
    start_halt = models.ForeignKey('Halt', on_delete=models.PROTECT,
                                   related_name='+')
    ## Arrêt de destination.
    end_halt = models.ForeignKey('Halt', on_delete=models.PROTECT,
                                 related_name='+')
    ## Voyage contenant le billet.
    travel = models.ForeignKey('Travel', on_delete=models.CASCADE)

    class Meta:
        """Métadonnées du modèle de billet de train."""
        ## Ordre par défaut si aucune clause order_by() n'est spécifiée dans
        #  un QuerySet.
        ordering = ["travel", "sequence"]
        ## Contrainte d'unicité assurant qu'un voyage ne contienne pas
        #  plusieurs billets avec la même position dans l'itinéraire.
        unique_together = ("travel", "sequence")
        ## Nom affiché dans l'interface d'administration de Django.
        verbose_name = "billet"
        ## Tri automatique lors de l'utilisation de earliest() ou latest()
        #  dans un QuerySet.
        get_latest_by = "sequence"

    @property
    def distance(self):
        """Distance parcourue en kilomètres."""
        return self.start_halt.station.distance_to(self.end_halt.station)

    @property
    def price(self):
        """Prix du billet."""
        return self.distance * self.start_halt.train.traintype.km_price

    def __str__(self):
        """Représentation textuelle du billet pour affichage."""
        return "Billet de " + str(self.start_halt) + " à " + \
            str(self.end_halt) + " le " + str(self.travel.date) + \
            " pour " + str(self.travel.user)


class Travel(models.Model):
    """
    Décrit un voyage. Un voyage peut contenir plusieurs billets, qui feront
    une correspondance.
    """
    ## Date du voyage.
    date = models.DateField()
    ## Nombre de passagers du voyage.
    passengers = models.PositiveSmallIntegerField(default=1)
    ## Association avec un utilisateur.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Métadonnées du modèle de voyage."""
        ## Tri par défaut si aucune clause order_by() n'est spécifiée dans un
        #  QuerySet.
        ordering = ["date", "user"]
        ## Nom affiché dans l'interface d'administration de Django.
        verbose_name = "voyage"

    @property
    def start_station(self):
        """Station de départ du voyage."""
        return self.ticket_set.order_by('sequence')[0].start_halt.station

    @property
    def end_station(self):
        """Station d'arrivée du voyage."""
        return self.ticket_set.order_by('-sequence')[:1].get().end_halt.station

    @property
    def start_time(self):
        """Heure de départ du voyage."""
        return self.ticket_set.order_by('sequence')[0].start_halt.departure

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

    def __str__(self):
        """Représentation textuelle du voyage pour affichage."""
        # S'il n'y a pas encore de billets dans le voyage (cas de la création
        # manuelle dans l'interface d'administration de Django),
        # "Voyage vide" est indiqué. Voir l'issue #23.
        return ("Voyage vide" if not self.ticket_set.count() else
                "Voyage de " + str(self.start_station) + " à " +
                str(self.end_station)) + \
            " le " + str(self.date) + " pour " + \
            str(self.passengers) + " passagers"
