# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from .models import Train, TrainType, Halt, Station, Period, PeriodException
from django.conf import settings


class TchouAdminSite(AdminSite):
    site_header = "Administration de TchouTchouGo"
    site_title = "TchouTchouGo Admin"
    index_title = "Accueil"
    index_template = settings.BASE_DIR + "/main/templates/admin/index.html"

admin_site = TchouAdminSite()
admin_site.register(TrainType)
admin_site.register(Period)
admin_site.register(PeriodException)
admin_site.register(Train)
admin_site.register(Station)
admin_site.register(Halt)
admin_site.register(Group)
admin_site.register(User)
