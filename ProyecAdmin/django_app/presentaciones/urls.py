from django.urls import path
from . import views

urlpatterns = [
    #path('archivos/', PresentacionListView.as_view(), name='archivo_texto_list'),
    path('presentaciones/', views.presentaciones, name='presentaciones'),
]