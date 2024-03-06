from django.shortcuts import render
#
from django.views.generic import ListView
#
from .models import Presentacion

class PresentacionListView(ListView):
    model = Presentacion
    template_name = 'presentacion_list.html' 
    context_object_name = 'archivos'

    def get_queryset(self):
        return Presentacion.objects.only('nombre', 'archivo')


