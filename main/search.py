# -*- coding: utf-8 -*-
"""Fonctions de recherche d'itinéraire de trains"""

from enum import Enum
from datetime import datetime, date
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
    zero = _search_zero(
        start_station, end_station, date, time, passengers, time_setting)
    if len(zero):
        return zero
    one = _search_one(
        start_station, end_station, date, time, passengers, time_setting)
    zero.extend(one)
    return zero


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
            tv.passengers_aboard.add(*passengers)
            Ticket.objects.create(start_halt=start_halt, end_halt=end_halt,
                                  sequence=0, travel=tv)
            travels.append(tr)
    return travels


def _search_one(start_station, end_station, date, time, passengers,
                time_setting=TimeOptions.DEPART_AFTER):
    """Effectuer une recherche d'itinéraire avec une correspondance.
    Renvoie des Travel correspondant aux résultats."""

    halt_ids = sql_query(
        """SELECT start_halt_id, mid1_halt_id, mid2_halt_id, end_halt_id,
        D.departure, D.first_arrival, A.second_departure, A.arrival FROM (
            SELECT start_halt_id, mid1_halt_id, I1.station_id as mid_station,
            D.departure, I1.arrival as first_arrival, first_train_id FROM (
                SELECT id AS start_halt_id, departure, sequence, train_id
                AS first_train_id FROM main_halt
                WHERE station_id = %s ) AS D INNER JOIN (
                SELECT id AS mid1_halt_id, station_id, arrival, sequence,
                train_id FROM main_halt ) AS I1
                ON first_train_id = I1.train_id AND D.sequence < I1.sequence
        ) AS D INNER JOIN (
            SELECT mid2_halt_id, end_halt_id, I2.station_id as mid_station,
            I2.departure as second_departure, A.arrival, second_train_id FROM (
                SELECT id AS mid2_halt_id, station_id, departure, sequence,
                train_id FROM main_halt ) AS I2 INNER JOIN (
                SELECT id AS end_halt_id, arrival, sequence,
                train_id AS second_train_id FROM main_halt
                WHERE station_id = %s ) AS A
                ON second_train_id = I2.train_id AND I2.sequence < A.sequence
        ) AS A ON D.mid_station = A.mid_station
        AND D.first_arrival < A.second_departure
        WHERE first_train_id <> second_train_id AND """ + time_setting.value +
        """ BETWEEN %s AND %s ORDER BY D.departure ASC, A.arrival ASC;""",
        [start_station.id, end_station.id,
         str(time.hour - 1) + ":00:00", str(time.hour + 1) + ":00:00"])

    # Filtrer pour ne garder que les trains qui circulent à la date souhaitée,
    # et ont assez de place, et créer les résultats de recherche correspondants
    travels = []
    for trip in halt_ids:
        mid_halt_1 = Halt.objects.get(id=trip[1])
        mid_halt_2 = Halt.objects.get(id=trip[2])
        if (datetime.combine(date.today(), mid_halt_2.departure) -
            datetime.combine(date.today(), mid_halt_1.arrival)) \
                .seconds / 3600 > 3:
            # Ignorer un temps de correspondance supérieur à 3 heures
            continue
        start_halt = Halt.objects.get(id=trip[0])
        end_halt = Halt.objects.get(id=trip[3])
        tr_1 = start_halt.train
        tr_2 = end_halt.train
        if tr_1.runs(date) and tr_2.runs(date) and \
                tr_1.can_hold(start_halt, mid_halt_1, len(passengers)) and \
                tr_2.can_hold(mid_halt_2, end_halt, len(passengers)):
            tv = Travel.objects.create(date=date, user=None, booked=False)
            tv.passengers_aboard.add(*passengers)
            Ticket.objects.create(start_halt=start_halt, end_halt=mid_halt_1,
                                  sequence=0, travel=tv)
            Ticket.objects.create(start_halt=mid_halt_2, end_halt=end_halt,
                                  sequence=1, travel=tv)
            travels.append(tv)
    return travels
