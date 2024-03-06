from django.urls import path
from .views import PresentacionListView

urlpatterns = [
    path('archivos/', PresentacionListView.as_view(), name='archivo_texto_list'),
]