from django.conf.urls import url

from app import views

urlpatterns = [
    # ex: /polls/
url(r'^$', views.index, name='index'),
url(r'^login$', views.login, name='login'),
url(r'^signup$', views.signup, name='signup'),
url(r'^vendedor$', views.vendedor, name='vendedor'),
url(r'^gestionproductos$', views.gestion, name='gestionproductos'),
]