from django.shortcuts import render
from .models import Presentacion
from django.views.generic import ListView
from .forms import CrearArchivoForm
from .forms import CrearArchivoForm
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
from django.contrib import messages

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
        titulo = request.POST.get('tituloPresentacion', '')
        contenido = request.POST.get('contenidoPresentacion', '')

        # Aquí se escribe el contenido en el archivo de texto
        try:
            # Directorio donde se almacenarán los archivos de texto
            directorio = 'PresentacionesTXT'
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            
            # Ruta del archivo de texto
            ruta_archivo = os.path.join(directorio, f'{titulo}.txt')

            # Escribir el contenido en el archivo
            with open(ruta_archivo, 'w') as archivo:
                archivo.write(contenido)

            # Mensaje de éxito
            mensaje = 'La presentación se generó correctamente.'
            return render(request, 'Presentaciones.html', {'mensaje': mensaje})
        except Exception as e:
            # Mensaje de error
            mensaje = f'Error al generar el archivo: {e}'
            return render(request, 'Presentaciones.html', {'mensaje': mensaje})

    return HttpResponse('No se pudo generar el archivo')

def presentaciones(request):
    return render(request, 'Presentaciones.html')

def lista_presentaciones(request):
    # Directorio donde se encuentran los archivos de texto
    directorio = os.path.join(settings.BASE_DIR, 'PresentacionesTXT')

    # Obtener una lista de todos los archivos en el directorio
    archivos = os.listdir(directorio)

    # Pasar la lista de archivos a la plantilla
    return render(request, 'presentacion_list.html', {'archivos': archivos})
