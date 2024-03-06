from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('registro/', views.register, name='registro'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('inicio/', views.inicio, name='inicio'),
    path('administrador/', views.administrador, name='administrador'),

]
