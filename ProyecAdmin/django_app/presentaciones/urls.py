from django.urls import path
from . import views
from usuarios.views import administrador

urlpatterns = [
    #path('archivos/', PresentacionListView.as_view(), name='archivo_texto_list'),
    path('presentaciones/', views.presentaciones, name='presentaciones'),
    path('crear_archivo/', views.crear_archivo, name='crear_archivo'),
    path('lista_presentaciones/', views.lista_presentaciones, name='lista_presentaciones'),
    path('editar_presentacion/', views.editar_presentacion, name='editar_presentacion'),
    path('eliminar_archivo/<str:nombre_archivo>/', views.eliminar_archivo, name='eliminar_archivo'),
    path('ver_presentacion/', views.ver_presentacion, name='ver_presentacion'),
    path('administrador/', administrador, name='administrador'),
]