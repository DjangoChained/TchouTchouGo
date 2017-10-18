# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.models import User, Group
from django.conf import settings
from . import models


class TicketAdmin(ModelAdmin):
    list_display = ('travel', 'sequence',)
    raw_id_fields = ('start_halt', 'end_halt',)


class TchouAdminSite(AdminSite):
    site_header = "Administration de TchouTchouGo"
    site_title = "TchouTchouGo Admin"
    index_title = "Accueil"
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
admin_site.register(Group)
admin_site.register(User)
