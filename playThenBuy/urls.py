from django.conf.urls import patterns, include, url

from django.contrib import admin
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib.auth import views as auth_views 



urlpatterns = patterns('',

    url(r'^$', 'principal.views.index'),                   
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^listadoJuegos/', 'principal.views.listadoJuegos'),
    url(r'^buscarTitulo/', 'principal.views.buscarTitulo'),
    url(r'^orderLanzamientoAsc/', 'principal.views.orderLanzamientoAsc'),
    url(r'^orderLanzamientoDesc/', 'principal.views.orderLanzamientoDesc'),
    url(r'^orderTituloAsc', 'principal.views.orderTituloAsc'),
    url(r'^orderTituloDesc/', 'principal.views.orderTituloDesc'),
    url(r'^orderPesoAsc/', 'principal.views.orderPesoAsc'),
    url(r'^orderPesoDesc/', 'principal.views.orderPesoDesc'),
    url(r'^orderDesarrolladoraAsc/', 'principal.views.orderDesarrolladoraAsc'),
    url(r'^orderDesarrolladoraDesc/', 'principal.views.orderDesarrolladoraDesc'),
    url(r'^orderPrecioDesc/', 'principal.views.orderPrecioDesc'),
    url(r'^orderPrecioAsc/', 'principal.views.orderPrecioAsc'),
    url(r'^filtros/', 'principal.views.filtros'),
    url(r'^juego/', 'principal.views.juego'),
    url(r'^puntua/', 'principal.views.puntua'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$',auth_views.logout, {'next_page': '/login'}),
    url(r'^obtenerTweets/$','principal.views.obtenerTweets'),
    
)
