from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'users$', views.index),
    url(r'users/new$',views.new),
    url(r'users/login$',views.login),
    url(r'users/error$',views.error),
    url(r'users/(?P<id>\d+)/destroy$',views.destroy),
    url(r'users/(?P<id>\d+)/edit$',views.edit),
    url(r'users/(?P<id>\d+)$',views.show),
    url(r'users/create$',views.create),
    url(r'users/update$',views.update)
]
