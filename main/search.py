# -*- coding: utf-8 -*-
"""Fonctions de recherche d'itinéraire de trains"""

from enum import Enum
from datetime import date
from time import strftime
from .utility import sql_query
from .models import Train, Halt, Travel, Ticket


class TimeOptions(Enum):
    """Définit les options de temps. Permet d'effectuer un départ après l'heure
    fournie ou une arrivée avant l'heure fournie."""
    ## Partir après une heure donnée.
    DEPART_AFTER = 'D.departure'
    ## Arriver avant une heure donnée.
    ARRIVE_BEFORE = 'A.arrival'


def search(start_station, end_station, date, time, passengers,
           time_setting=TimeOptions.DEPART_AFTER):
    """Effectuer une recherche d'itinéraire d'une gare à une autre, à une date
    donnée et une heure donnée et selon les paramètres de temps.
    Renvoie des objets Travel."""
    return _search_zero(
        start_station, end_station, date, time, passengers, time_setting)


def _search_zero(start_station, end_station, date, time, passengers,
                 time_setting=TimeOptions.DEPART_AFTER):
    """Effectuer une recherche d'itinéraire sans correspondances.
    Renvoie des Travel correspondant aux résultats."""

    halt_ids = sql_query(
        """SELECT start_halt_id, end_halt_id, D.train_id FROM (
    SELECT id AS start_halt_id, departure, sequence, train_id FROM main_halt
    WHERE station_id = %s) AS D INNER JOIN (
        SELECT id AS end_halt_id, arrival, sequence, train_id FROM main_halt
        WHERE station_id = %s) AS A
    ON D.train_id = A.train_id AND D.sequence < A.sequence
    WHERE """ + time_setting.value + """ BETWEEN %s AND %s
    ORDER BY departure ASC, arrival ASC""",
        [start_station.id, end_station.id,
         str(time.hour - 1) + ":00:00", str(time.hour + 1) + ":00:00"])

    # Filtrer pour ne garder que les trains qui circulent à la date souhaitée,
    # et créer les résultats de recherche correspondants
    travels = []
    for trip in halt_ids:
        tr = Train.objects.get(id=trip[2])
        start_halt = Halt.objects.get(id=trip[0])
        end_halt = Halt.objects.get(id=trip[1])
        if tr.runs(date) and \
                tr.can_hold(start_halt, end_halt, len(passengers)):
            tv = Travel.objects.create(date=date, user=None, booked=False)
            tr.passengers_aboard.add(*passengers)
            Ticket.objects.create(start_halt=start_halt, end_halt=end_halt,
                                  sequence=0, travel=tr)
            travels.append(tr)
    return travels
