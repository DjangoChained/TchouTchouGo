# -*- coding: utf-8 -*-
"""Formulaires de l'application."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Station
from .models import Passenger
from django.core.exceptions import ValidationError


def validate_station(value):
    if not value or not Station.objects.filter(name=value).exists():
        raise ValidationError("La gare de %(value)s n'existe pas.",
                              code='notfound', params={'value': value})


class SearchForm(forms.Form):
    """Formulaire de recherche de trajets."""
    ## Options disponibles pour l'heure
    #  Permet de demander à l'utilisateur s'il veut partir après ou arriver
    #  avant l'heure qu'il spécifie.
    TIME_OPTIONS = [
        ('DEPART_AFTER', 'Partir après'),
        ('ARRIVE_BEFORE', 'Arriver avant')
    ]
    ## Champ indiquant le nom de la gare de départ.
    startStation = forms.CharField(max_length=40, required=True,
                                   validators=[validate_station])
    ## Champ indiquant le nom de la gare d'arrivée.
    endStation = forms.CharField(max_length=40, required=True,
                                 validators=[validate_station])
    ## Champ indiquant la date souhaitée du voyage.
    travelDate = forms.DateField(required=True)
    ## Champ utilisé pour les options de l'heure (voir TIME_OPTIONS).
    timeOptions = forms.ChoiceField(choices=TIME_OPTIONS)
    ## Champ utilisé pour la sélection du créneau horaire.
    hour = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(5, 22)])
    ## Champ utilisé pour le nombre de passagers.
    passengers = forms.IntegerField(min_value=1, max_value=9)


class SignUpForm(UserCreationForm):
    """Formulaire d'inscription à l'application."""
    ## Champ du prénom de l'utilisateur
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional.')
    ## Champ du nom de l'utilisateur
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional.')
    ## Champ pour l'adresse e-mail de l'utilisateur
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        """Métadonnées du formulaire d'inscription à l'application."""
        ## Modèle associé au formulaire.
        model = User
        ## Indiquer les champs du formulaire.
        #  Permet d'hériter automatiquement des champs depuis le formulaire
        #  par défaut pour l'utilisateur Django.
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2', )


class UserForm(forms.ModelForm):
    """Formulaire de mise à jour d'un profil utilisateur."""
    class Meta:
        """Métadonnées du formulaire de mise à jour d'utilisateur."""
        ## Modèle associé au formulaire.
        model = User
        ## Champs associés au formulaire.
        #  Permet d'hériter automatiquement des champs depuis le formulaire
        #  par défaut pour l'utilisateur Django.
        fields = ('first_name', 'last_name', 'email')


class PassengerForm(forms.ModelForm):
    """Formulaire de mise à jour d'un passager """

    ## Champ du prénom du passager
    first_name = forms.CharField(max_length=30, required=True)
    ## Champ du nom du passager
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        """Métadonnées du formulaire de mise à jour d'un passager"""
        ## Modèle associé au formulaire.
        model = Passenger
        ##Champs associés au formulaire.
        fields = ('first_name', 'last_name')
