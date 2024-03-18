from django.shortcuts import render
from .models import Presentacion
from django.views.generic import ListView
from .forms import CrearArchivoForm
from .forms import CrearArchivoForm
import os
from django.conf import settings
#
from django.views.generic import ListView
#
#from .models import Presentacion

#def PresentacionListView(ListView):
#   model = Presentacion
#   template_name = 'presentacion_list.html' 
#   context_object_name = 'archivos'
#   def get_queryset(self):
#       return Presentacion.objects.only('nombre', 'archivo')

#def crear_archivo(request):
#    if request.method == 'POST':
#        form = CrearArchivoForm(request.POST)
#        if form.is_valid():
#            nombre_archivo = form.cleaned_data['nombre_archivo']
#            contenido = form.cleaned_data['contenido']
#            ruta_archivo = f"/ProyecAdmin/django_app/PresentacionesTXT/{nombre_archivo}.txt"  # Ruta predefinida con el nombre asignado
#            with open(ruta_archivo, 'w') as archivo:
#                archivo.write(contenido)
#            return render(request, 'archivo_creado.html', {'ruta_archivo': ruta_archivo})
#    else:
#        form = CrearArchivoForm()
#    return render(request, 'crear_archivo.html', {'form': form})

# Create your views here.

def crear_archivo(request):
    if request.method == 'POST':
        form = CrearArchivoForm(request.POST)
        if form.is_valid():
            nombre_archivo = form.cleaned_data['nombre_archivo']
            contenido = form.cleaned_data['contenido']
            ruta_archivo = f"/ProyecAdmin/django_app/PresentacionesTXT/{nombre_archivo}.txt"  # Ruta predefinida con el nombre asignado
            with open(ruta_archivo, 'w') as archivo:
                archivo.write(contenido)
            return render(request, 'archivo_creado.html', {'ruta_archivo': ruta_archivo})
    else:
        form = CrearArchivoForm()
    return render(request, 'crear_archivo.html', {'form': form})

def presentaciones(request):
   return render(request, 'Presentaciones.html')

def presentaciones_view(request):
    presentaciones_dir = os.path.join(settings.BASE_DIR, 'PresentacionesTXT')
    presentaciones = os.listdir(presentaciones_dir)
    return render(request, 'presentacion_list.html', {'presentaciones': presentaciones})
