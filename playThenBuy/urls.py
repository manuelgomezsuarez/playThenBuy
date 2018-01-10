from django.conf.urls import patterns, include, url
from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'principal.views.index'),                   
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^listadoJuegos', 'principal.views.listadoJuegos'),
    url(r'^buscarTitulo', 'principal.views.buscarTitulo'),
    
)
