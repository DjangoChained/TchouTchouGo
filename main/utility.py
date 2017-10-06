#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fonctions utilitaires pour l'application TchouTchouGo.
"""
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculer la distance entre deux coordonnées GPS sur Terre en utilisant la
    formule Haversine. Honteusement volé depuis StackOverflow.
    https://stackoverflow.com/questions/4913349/
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km
