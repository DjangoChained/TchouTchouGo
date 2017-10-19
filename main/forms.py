# -*- coding: utf-8 -*-
"""Formulaires de l'application."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    """Formulaire de recherche de trajets."""
    ## Options disponibles pour l'heure
    #  Permet de demander à l'utilisateur s'il veut partir après ou arriver
    #  avant l'heure qu'il spécifie.
    TIME_OPTIONS = [
        ('leaveAfter', 'Partir après'),
        ('arriveBefore', 'Arriver avant')
    ]
    ## Champ indiquant le nom de la gare de départ.
    startStation = forms.CharField(max_length=40, required=True)
    ## Champ indiquant le nom de la gare d'arrivée.
    endStation = forms.CharField(max_length=40, required=True)
    ## Champ indiquant la date souhaitée du voyage.
    travelDate = forms.DateField(required=True)
    ## Champ utilisé pour les options de l'heure (voir TIME_OPTIONS).
    timeOptions = forms.ChoiceField(choices=TIME_OPTIONS)
    ## Champ utilisé pour la sélection du créneau horaire.
    hour = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(5, 22)])


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
