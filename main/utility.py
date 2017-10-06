#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Fonctions utilitaires pour l'application TchouTchouGo.
"""

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
