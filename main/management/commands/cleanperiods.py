# -*- coding: utf-8 -*-
"""
Commande de nettoyage des périodes de service.
"""
from django.core.management.base import BaseCommand
from main.models import Period, PeriodException


class Command(BaseCommand):
    help = 'Nettoyage automatique des périodes de service inutilisées'

    def handle(self, *args, **options):
    	oldcount = Period.objects.count()
        [p.delete() for p in Period.objects.all() if p.train_set.count() == 0]
        newcount = Period.objects.count()
        self.stdout.write(self.style.SUCCESS(
            'Nettoyage des périodes de service effectué. ' + \
            (oldcount - newcount) + ' périodes supprimées.'))