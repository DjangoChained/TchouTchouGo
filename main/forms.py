# -*- coding: utf-8 -*-
"""Formulaires de l'application."""
from django import forms


class SearchForm(forms.Form):
    TIME_OPTIONS = [
        ('leaveAfter', 'Partir après'),
        ('arriveBefore', 'Arriver avant')
    ]
    startStation = forms.CharField(max_length=40, required=True)
    endStation = forms.CharField(max_length=40, required=True)
    travelDate = forms.DateField(required=True)
    timeOptions = forms.ChoiceField(choices=TIME_OPTIONS)
    hour = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(5, 22)])
