# -*- coding: utf-8 -*-
"""Formulaires de l'application."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2', )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
