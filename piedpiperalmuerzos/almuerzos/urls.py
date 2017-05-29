from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^$', views.base, name = 'base'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name = 'signup'),
    url(r'^gestion_productos/$', views.gestion_productos, name = 'gestion_productos'),
    url(r'^vendedor_perfil/$', views.vendedor_perfil, name = 'vendedor_perfil'),
    url(r'^auth/$', views.auth_view, name = 'autenticacion'),
    url(r'^registration/$', views.registration, name = 'registration'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^edit_auth/$', views.edit_auth, name='edit_auth'),

]
