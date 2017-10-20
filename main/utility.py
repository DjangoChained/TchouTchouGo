#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fonctions utilitaires pour l'application TchouTchouGo.
"""

from math import radians, cos, sin, asin, sqrt
from django.db import connection
import os


def remove_if_exists(filename):
    """Supprimer un fichier ou un dossier s'il existe. Sinon, ne rien faire.
    Si une erreur autre que 'fichier introuvable' se produit,
    l'erreur sera tout de même renvoyée."""
    try:
        os.remove(filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


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
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def sql_query(sql, params=None):
    """Exécuter une requête SQL directement. Voir la page d'aide :
    https://docs.djangoproject.com/fr/1.11/topics/db/sql/"""
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
    return rows
