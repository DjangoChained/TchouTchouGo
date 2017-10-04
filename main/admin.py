# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Train, TrainType, Halt, Station, Period, PeriodException

admin.site.register(TrainType)
admin.site.register(Period)
admin.site.register(PeriodException)
admin.site.register(Train)
admin.site.register(Station)
admin.site.register(Halt)
