from django.urls import path
from . import views
from presentaciones.views import presentaciones
from presentaciones.views import presentaciones_view

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('registro/', views.register, name='registro'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('inicio/', views.inicio, name='inicio'),
    path('administrador/', views.administrador, name='administrador'),
    path('presentaciones/', presentaciones, name='presentaciones'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('cambiar-rol/<int:usuario_id>/', views.cambiar_rol, name='cambiar_rol'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_cuenta, name='eliminar_usuario'),
    path('help/', views.help, name='help'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
<<<<<<< HEAD
    path('logout/', views.logout_view, name='logout'),
    path('presentaciones_lista/', presentaciones_view, name='presentaciones_lista'),


=======
    path('perfil/', views.perfil, name='perfil'),
>>>>>>> 7f8bfaaf9f9164cb6092d9e3f6351748220d3a68
]
