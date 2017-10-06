# -*- coding: utf-8 -*-

import zipfile
import os
import csv
from datetime import date, time
from .utility import remove_if_exists
from .models import Period
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
    """Créer un objet Period correspondant à une ligne du fichier calendar
    du format GTFS."""
    p = []
    for line in lines:
        if Period.objects.filter(id=int(line[0])).exists():
            continue
        p.append(Period.objects.create(id=int(line[0]),
                                       monday=(line[1] == '1'),
                                       tuesday=(line[2] == '1'),
                                       wednesday=(line[3] == '1'),
                                       thursday=(line[4] == '1'),
                                       friday=(line[5] == '1'),
                                       saturday=(line[6] == '1'),
                                       sunday=(line[7] == '1'),
                                       start_date=parse_gtfs_date(line[8]),
                                       end_date=parse_gtfs_date(line[9])))
    for per in p:
        per.save()
