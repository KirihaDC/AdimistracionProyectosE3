from django.urls import path
from . import views
from presentaciones.views import presentaciones

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('registro/', views.register, name='registro'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('change-password/<int:user_id>/', views.change_password, name='change_password'),
    path('inicio/', views.inicio, name='inicio'),
    path('administrador/', views.administrador, name='administrador'),
    path('presentaciones/', presentaciones, name='presentaciones'),
    path('lista_usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('cambiar-rol/<int:usuario_id>/', views.cambiar_rol, name='cambiar_rol'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_cuenta, name='eliminar_usuario'),
    path('help/', views.help, name='help'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('perfil/', views.perfil, name='perfil'),
    path('leer_archivo/', views.leer_archivo, name='leer_archivo'),
    path('eliminar_perfil/', views.eliminar_perfil, name='eliminar_perfil'),
    path('registro_usuarios/', views.registro_usuarios, name='registro_usuarios'),
    path('lista_presentacionesUsurario/', views.lista_presentacionesUsuario, name='lista_presentacionesUsuario'),
]

