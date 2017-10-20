# -*- coding: utf-8 -*-
"""
Commande de nettoyage des trains.
Les trains sont supprimés s'ils ne sont plus en circulation et qu'ils n'ont
pas eu de réservations.
"""
from django.core.management.base import BaseCommand
from main.models import Train
from datetime import datetime


class Command(BaseCommand):
    help = 'Nettoyage automatique des trains sans réservations'

    def handle(self, *args, **options):
        oldcount = Train.objects.count()
        [t.delete() for t in Train.objects.all()
         if t.period and datetime.now() > t.period.end_date and
         True not in [h.ticket_start_set.count() > 0
                      or h.ticket_end_set.count() > 0
                      for h in t.halt_set.all()]]
        newcount = Train.objects.count()
        self.stdout.write(self.style.SUCCESS(
            'Nettoyage des trains effectué. ' +
            str(oldcount - newcount) + ' trains supprimés.'))
