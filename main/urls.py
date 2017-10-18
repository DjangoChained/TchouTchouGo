from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/train/search', permanent=False)),
    url(r'^search$', views.search, name='search'),
    url(r'^searchResult$', views.searchResult, name='searchResult'),
    url(r'^tickets$', views.tickets, name='tickets'),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/train'},
        name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^updateProfile$', views.updateProfile, name="updateProfile")
]
