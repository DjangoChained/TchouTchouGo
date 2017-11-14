# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import basename
from django.shortcuts import render
from .admin_forms import GTFSImportForm
from main.gtfs_parser import parse_gtfs_sncf
from main.models import \
    Train, TrainType, Station, Halt, Period, PeriodException


def handle_uploaded_zip(f):
    with open('/tmp/' + basename(f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
        return '/tmp/' + basename(f.name)


def gtfs_import(request):
    form = GTFSImportForm(request.POST, request.FILES)
    if form.is_valid():
        ter_path = handle_uploaded_zip(request.FILES['zip_ter'])
        ic_path = handle_uploaded_zip(request.FILES['zip_ic'])
        if form.cleaned_data['clear_everything']:
            Halt.objects.all().delete()
            Station.objects.all().delete()
            Train.objects.all().delete()
            TrainType.objects.all().delete()
            PeriodException.objects.all().delete()
            Period.objects.all().delete()
        parse_gtfs_sncf(ter_path, ic_path)
        success = True

    site_header = "Administration de TchouTchouGo"
    site_title = "TchouTchouGo Admin"
    title = "Importation GTFS"
    return render(request, 'admin/gtfs_import.html', locals())
