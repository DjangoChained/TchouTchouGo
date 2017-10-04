from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/train/search', permanent=False)),
    url(r'^search$', views.search, name='search'),
]
