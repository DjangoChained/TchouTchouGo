# -*- coding: utf-8 -*-
"""
Commande de nettoyage des stations.
Les stations sont supprimées si elles n'ont aucun train s'y arrêtant.
"""
from django.core.management.base import BaseCommand
from main.models import Station


class Command(BaseCommand):
    help = 'Nettoyage automatique des stations inutilisées'

    def handle(self, *args, **options):
        oldcount = Station.objects.count()
        [s.delete() for s in Station.objects.all() if s.halt_set.count() == 0]
        newcount = Station.objects.count()
        self.stdout.write(self.style.SUCCESS(
            'Nettoyage des stations effectué. ' +
            str(oldcount - newcount) + ' stations supprimées.'))
