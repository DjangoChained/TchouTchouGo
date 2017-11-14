# -*- coding: utf-8 -*-
"""
Commande de nettoyage des résultats de recherche.
Les résultats de recherche sont traduits sous la forme de voyages non réservés.
Les voyages non réservés sont supprimés.
"""
from django.core.management.base import BaseCommand
from main.models import Travel


class Command(BaseCommand):
    help = 'Nettoyage automatique des périodes de service inutilisées'

    def handle(self, *args, **options):
        oldcount = Travel.objects.count()
        for t in Travel.objects.all():
            if not t.booked:
                t.delete()
            else if t.user is None:
                self.stderr.write(self.style.WARNING(
                    "Le voyage ayant l'ID " + t.id +
                    " est marqué comme réservé, "
                    "mais n'a pas de passager associé."))
        [p.delete() for p in Period.objects.all() if p.train_set.count() == 0]
        newcount = Travel.objects.count()
        self.stdout.write(self.style.SUCCESS(
            'Nettoyage des voyages non réservés effectués. ' +
            str(oldcount - newcount) + ' voyages supprimés.'))
