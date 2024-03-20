from django.urls import path
from . import views

urlpatterns = [
    #path('archivos/', PresentacionListView.as_view(), name='archivo_texto_list'),
    path('presentaciones/', views.presentaciones, name='presentaciones'),
    path('lista_presentaciones/', views.lista_presentaciones, name='lista_presentaciones')
]