from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.index, name='index'),
    path('fill', views.fill, name='fill'),
    #path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getResult', views.getResult, name='getResult'),
    path('register', views.register, name="register"),
    path('getData', views.getData, name='getData'),
    path('getData_wrong', views.getData_wrong, name='getData_wrong'),
    path('registData', views.registData, name="registData"),
    path('toCSV', views.toCSV, name="toCSV"),
    path('modify', views.modify, name="modify"),
    path('update/<str:id>', views.update, name="update"),
    path('search', views.search, name="search"),
    path('delete', views.delete, name="delete"),
    path('choice', views.choice, name="choice"),
    path('judge', views.judge, name="judge"),

    path('config', views.config, name="config"), 
]