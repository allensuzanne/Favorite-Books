from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^books/(?P<book_id>\d+)$', views.books_id),
    url(r'^books/ad$', views.books_ad),
    url(r'^books/(?P<book_id>\d+)/update$', views.books_id_update),
    url(r'^favorite/(?P<book_id>\d+)$', views.favorite),
    url(r'^unfavorite/(?P<book_id>\d+)$', views.unfavorite),
    url(r'^books/(?P<book_id>\d+)/destroy$', views.destroy),
    url(r'^books/(?P<book_id>\d+)/edit$', views.books_id_edit),
]