# -*- coding: utf-8 -*-
from django import forms


class GTFSImportForm(forms.Form):
    zip_ter = forms.FileField(
        allow_empty_file=False, label="Archive TER", required=True,
        help_text="Archive au format ZIP fournie par la SNCF et contenant "
                  "les données d'horaires des TER au format GTFS."
    )
    zip_ic = forms.FileField(
        allow_empty_file=False, label="Archive IC", required=True,
        help_text="Archive au format ZIP fournie par la SNCF et contenant "
                  "les données d'horaires des Intercités au format GTFS."
    )
    clear_everything = forms.BooleanField(
        label="Effacer tout", required=False,
        help_text="Effacer l'intégralité des données ferroviaires avant de "
                  "procéder à l'importation."
    )
