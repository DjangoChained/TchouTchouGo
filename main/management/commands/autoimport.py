# -*- coding: utf-8 -*-
"""
Commande d'importation automatique GTFS.
Les dernières données Open Data SNCF pour les horaires TER et Intercités sont
téléchargées automatiquement et l'importation GTFS s'enclenche immédiatement.
Destiné à un usage en CRON, une fois par mois.
"""
from django.core.management.base import BaseCommand
from main.gtfs_parser import parse_gtfs_sncf


def get_file_url(dataset):
    """Récupérer une URL de téléchargement de fichier ZIP à partir du nom
    du dataset."""
    BASE_URL = "https://data.sncf.com/api/records/1.0/search/?dataset="
    FILE_URL = "https://data.sncf.com/explore/dataset/{}/files/{}/download/"
    import urllib.request
    import json
    with urllib.request.urlopen(BASE_URL + dataset) as response:
        data = json.loads(response.read().decode())
    return FILE_URL.format(dataset,
                           data['records'][0]['fields']['download']['id'])


class Command(BaseCommand):
    help = 'Nettoyage automatique des périodes de service inutilisées'

    def handle(self, *args, **options):
        DATASETS = ['sncf-ter-gtfs', 'sncf-intercites-gtfs']
        import urllib
        [urllib.urlretrieve(get_file_url(dataset), '/tmp/' + dataset + '.zip')
            for dataset in DATASETS]
        parse_gtfs_sncf(['/tmp/' + dataset + '.zip' for dataset in DATASETS])
        self.stdout.write(self.style.SUCCESS(
            'Importation automatique GTFS effectuée.'))
