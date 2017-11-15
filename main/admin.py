# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.models import User, Group
from django.conf import settings
from . import models


class TicketAdmin(ModelAdmin):
    """Gestionnaire d'administration des billets de train."""
    ## Colonnes affichées pour décrire un billet.
    list_display = ('travel', 'sequence',)
    ## Champs n'affichant pas une sélection par dropdown.
    raw_id_fields = ('start_halt', 'end_halt',)


class TchouAdminSite(AdminSite):
    """Paramètres des fonctionnalités d'administration de l'application."""
    ## En-tête du site d'administration.
    site_header = "Administration de TchouTchouGo"
    ## Titre du site
    site_title = "TchouTchouGo Admin"
    ## Titre de la page d'accueil
    index_title = "Accueil"
    ## Template utilisé pour la page d'accueil
    index_template = settings.BASE_DIR + "/main/templates/admin/index.html"

admin_site = TchouAdminSite()
admin_site.register(models.TrainType)
admin_site.register(models.Period)
admin_site.register(models.PeriodException)
admin_site.register(models.Train)
admin_site.register(models.Station)
admin_site.register(models.Halt)
admin_site.register(models.Ticket, admin_class=TicketAdmin)
admin_site.register(models.Travel)
admin_site.register(models.Passenger)
admin_site.register(Group)
admin_site.register(User)
