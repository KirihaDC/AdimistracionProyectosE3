from django.urls import path
from . import views
from usuarios.views import administrador

urlpatterns = [
    path('presentaciones/', views.presentaciones, name='presentaciones'),
    path('crear_archivo/', views.crear_archivo, name='crear_archivo'),
    path('lista_presentaciones/', views.lista_presentaciones, name='lista_presentaciones'),
    path('editar_presentacion/', views.editar_presentacion, name='editar_presentacion'),
    path('eliminar_archivo/<str:nombre_archivo>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('ver_presentacion/', views.ver_presentacion, name='ver_presentacion'),
    path('upload/', views.upload_file, name='upload_file'),  # Nueva ruta para la subida de archivos
    path('administrador/', administrador, name='administrador'),
]
