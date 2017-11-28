from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/train/search', permanent=False)),
    url(r'^search$', views.search, name='search'),
    url(r'^stations.json$', views.stations_json, name='stations_json'),
    url(r'^tickets$', views.tickets, name='tickets'),
    url(r'^map$', views.full_map, name='map'),
    url(r'^stations.geojson$', views.full_map_geojson, name='map_geojson'),
    url(r'^map/travel/(\d+)$', views.travel_map, name='travel_map'),
    url(r'^travel(\d+).geojson', views.travel_map_geojson,
        name='travel_map_geojson'),
    url(r'^cart$', views.cart_show, name='cart'),
    url(r'^cart/add/(\d+)$', views.cart_add, name='cart_add'),
    url(r'^cart/remove/(\d+)$', views.cart_remove, name='cart_remove'),
    url(r'^order$', views.order, name='order'),
    url(r'^passengers$', views.passengers, name='passengers'),
    url(r'^addPassenger$', views.addPassenger, name='addPassenger'),
    url(r'^updatePassenger/(\d+)$', views.updatePassenger,
        name='updatePassenger'),
    url(r'^deletePassenger/(\d+)$', views.deletePassenger,
        name='deletePassenger'),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': '/train'},
        name='logout'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^print/(\d+)$', views.print_ticket, name='print_ticket'),
    url(r'^updateProfile$', views.update_profile, name='update_profile'),
    url(r'^updatePassword$', views.change_password, name='update_password'),
]
