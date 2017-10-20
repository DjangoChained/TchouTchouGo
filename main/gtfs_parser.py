# -*- coding: utf-8 -*-

import zipfile
import os
import csv
import re
from datetime import date, time
from .utility import remove_if_exists
from .models import Period, PeriodException, TrainType, Station, Train, Halt
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


def parse_gtfs_sncf(*args):
    """
    Prend en charge la conversion de plusieurs archives ZIP contenant des
    données GTFS en provenance de la SNCF.
    Passez en argument des chemins d'accès vers les archives ZIP GTFS.
    """
    print("Started parsing SNCF GTFS data.")
    for path in args:
        assert path.endswith('.zip')
        assert os.path.isfile(path)
        archive = zipfile.ZipFile(path, 'r')
        archive.extractall(path=path.replace('.zip', '/'))
        archive.close()
    folders = [p.replace('.zip', '/') for p in args]
    print("Unzipped archives.")
    for f in folders:
        print("Parsing " + f)
        assert os.path.exists(f + "calendar.txt")
        assert os.path.exists(f + "calendar_dates.txt")
        assert os.path.exists(f + "routes.txt")
        assert os.path.exists(f + "stops.txt")
        assert os.path.exists(f + "stop_times.txt")
        assert os.path.exists(f + "trips.txt")
        remove_if_exists(f + "agency.txt")
        remove_if_exists(f + "transfers.txt")
        print("Parsing " + f + "calendar.txt")
        parse_gtfs_calendar(csv_reader_skip_header(f + 'calendar.txt'))
        print("Parsing " + f + "calendar_dates.txt")
        parse_gtfs_calendar_dates(
            csv_reader_skip_header(f + 'calendar_dates.txt'))
        print("Parsing " + f + "stops.txt (first pass)")
        parse_gtfs_stops_traintype(csv_reader_skip_header(f + "stops.txt"))
        print("Parsing " + f + "stops.txt (second pass)")
        parse_gtfs_stops_station(csv_reader_skip_header(f + "stops.txt"))
        print("Parsing " + f + "trips.txt and " + f + "stop_times.txt")
        parse_gtfs_trains(
            csv_reader_skip_header(f + "trips.txt"), f + "stop_times.txt")


def csv_reader_skip_header(path):
    """Ouvrir un fichier CSV en lecture,
    et passer la ligne d'en-tête s'il y en a une."""
    file = open(path, "rb")
    has_header = csv.Sniffer().has_header(file.read(1024))
    file.seek(0)
    csvreader = csv.reader(file)
    if has_header:
        next(csvreader)
    return csvreader


def parse_gtfs_date(datestr):
    """Transformer une date GTFS en un objet datetime.date."""
    return date(int(datestr[:4]), int(datestr[4:6]), int(datestr[-2:]))


def parse_gtfs_calendar(lines):
    """Créer des objets Period correspondant au fichier calendar
    du format GTFS."""
    p = []
    for line in lines:
        if Period.objects.filter(id=int(line[0])).exists():
            continue
        p.append(Period(id=int(line[0]),
                        monday=(line[1] == '1'),
                        tuesday=(line[2] == '1'),
                        wednesday=(line[3] == '1'),
                        thursday=(line[4] == '1'),
                        friday=(line[5] == '1'),
                        saturday=(line[6] == '1'),
                        sunday=(line[7] == '1'),
                        start_date=parse_gtfs_date(line[8]),
                        end_date=parse_gtfs_date(line[9])))
    print("Writing to database...")
    [per.save() for per in p]


def parse_gtfs_calendar_dates(lines):
    """Créer des objets PeriodException correspondant au fichier
    calendar_dates du format GTFS."""
    pex = []
    for line in lines:
        p = Period.objects.filter(id=int(line[0]))
        if not p.exists():
            continue
        else:
            p = p.get()
        date = parse_gtfs_date(line[1])
        if PeriodException.objects.filter(period=p, date=date).exists():
            continue
        pex.append(PeriodException(date=date,
                                   add_day=line[2] == '1',
                                   period=p))
    print("Writing to database...")
    [ex.save() for ex in pex]


def parse_gtfs_stops_traintype(lines):
    """Créer des objets TrainType depuis les données du fichier stops.txt du
    format GTFS."""
    # L'expression régulière convertit un identifiant de station SNCF du type
    # StopPoint:OCETrain TER-87576173
    # en un type de train ("Train TER" dans l'exemple).
    regex = re.compile(r"^.*OCE(.*)-[0-9]+$", re.MULTILINE)
    # Une compréhension de liste utilisant lines va trier et ne récupérer que
    # les ID commençant par "StopPoint" puisque StopArea ne contient pas de
    # types de trains. Une seconde compréhension de liste va ensuite exécuter
    # l'expression régulière.
    # set() permet de supprimer les très nombreux doublons.
    # On reconvertit ensuite en liste avec list() pour créer des TrainTypes,
    # dans une troisième compréhension de liste, en évitant les doublons.
    traintypes = [TrainType(name=name) for name in list(set(
        [regex.sub('\\1', stopid) for stopid in
            [line[0] for line in lines if line[0].startswith("StopPoint")]]))
        if not TrainType.objects.filter(name=name).exists()]
    print("Writing to database...")
    [tt.save() for tt in traintypes]


def parse_gtfs_stops_station(lines):
    """Créer des objets Station depuis les données du fichier stops.txt du
    format GTFS."""
    id_regex = re.compile(r"^.*OCE.*-([0-9]+)$", re.MULTILINE)
    name_regex = re.compile(r"^(gare de)? (.*)$", re.MULTILINE)
    stations = [Station(id=int(id_regex.sub('\\1', line[0])),
                        name=name_regex.sub('\\2', line[1]),
                        lat=line[3], lng=line[4])
                for line in lines
                if line[0].startswith("StopPoint") and not Station.objects
                .filter(id=int(id_regex.sub('\\1', line[0]))).exists()]
    print("Writing to database...")
    [s.save() for s in stations]


def parse_gtfs_trains(trips, stop_times_path):
    """Créer des objets Train et Halt correspondant aux données des fichiers
    trips.txt et stop_times.txt du format GTFS.
    Attention : Cette méthode prend en paramètre un lecteur de fichiers CSV
    pour trips.txt et un chemin d'accès seulement pour stop_times.txt."""
    stop_times_file = open(stop_times_path)
    stop_times = csv.reader(stop_times_file)
    # Permet de trouver le type de train
    tt_regex = re.compile(r"^.*OCE(.*)-[0-9]+$", re.MULTILINE)
    trains, halts = [], []
    period_ids = Period.objects.values_list("id", flat=True)
    for trip in trips:
        stop_times_file.seek(1)
        trip_stop_times = [s for s in stop_times if s[0] == trip[2]]
        if int(trip[1]) in period_ids:
            p = int(trip[1])
        else:
            p = None
        t = Train(
            number=int(trip[3]), traintype=TrainType.objects.get(
                name=tt_regex.sub('\\1', trip_stop_times[0][3])))
        t.period_id = p
        trains.append(t)
        halts.extend(parse_gtfs_halts_train(trip[2], trip_stop_times, t.id))
    print("Writing to database...")
    [t.save() for t in trains]
    [h.save() for h in halts]


def parse_gtfs_halts_train(trip_id, stop_times, train_id):
    """Créer des objets Halt pour un train donné depuis les données du fichier
    stop_times.txt du format GTFS."""
    halts = []
    station_id_regex = re.compile(r"^.*OCE.*-([0-9]+)$", re.MULTILINE)
    for stop_time in stop_times:
        ar_time = stop_time[1].split(':', 2)
        ar_sec = time(hour=int(ar_time[0]) % 24, minute=int(ar_time[1]))
        dep_time = stop_time[2].split(':', 2)
        dep_sec = time(hour=int(dep_time[0]) % 24, minute=int(dep_time[1]))
        h = Halt(arrival=ar_sec, departure=dep_sec, sequence=stop_time[4])
        h.station_id = int(station_id_regex.sub('\\1', stop_time[3]))
        h.train_id = train_id
        halts.append(h)
    return halts
