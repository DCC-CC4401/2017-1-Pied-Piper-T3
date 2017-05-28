from django.conf.urls import url

from app import views

urlpatterns = [
    # ex: /polls/
url(r'^$', views.index, name='index'),
url(r'^login$', views.index, name='login'),
]