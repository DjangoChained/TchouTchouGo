"""TchouTchouGo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from main.admin import admin_site
from main import admin_views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin_site.urls),
    url(r'^admin/gtfs-import/?$', admin_views.gtfs_import, name="gtfs-import"),
    url(r'^$', RedirectView.as_view(url='/train/', permanent=False)),
    url(r'^train/', include('main.urls')),
]

handler500 = 'main.errors_views.handler500'
handler404 = 'main.errors_views.handler404'
handler403 = 'main.errors_views.handler403'
handler400 = 'main.errors_views.handler400'
