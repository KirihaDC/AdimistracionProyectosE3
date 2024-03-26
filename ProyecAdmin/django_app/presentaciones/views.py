from django.shortcuts import render
from .models import Presentacion
from django.views.generic import ListView
from .forms import CrearArchivoForm
from .forms import CrearArchivoForm
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from pathlib import Path
import re

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

def editar_presentacion(request):
    return render(request, 'editar_presentacion.html')

def ver_presentacion(request):
    return render(request, 'ver_presentacion.html')

def lista_presentaciones(request):
    # Directorio donde se encuentran los archivos de texto
    directorio = os.path.join(settings.BASE_DIR, 'PresentacionesTXT')

    # Obtener una lista de todos los archivos en el directorio
    archivos = os.listdir(directorio)

    # Pasar la lista de archivos a la plantilla
    return render(request, 'presentacion_list.html', {'archivos': archivos})

def eliminar_archivo(request, nombre_archivo):
    ruta_archivo = os.path.join(settings.BASE_DIR, 'PresentacionesTXT', nombre_archivo)
    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)
        return redirect('lista_presentaciones')
    else:
        return redirect('lista_presentaciones')

def editar_presentacion(request):
    nombre_archivo = request.GET.get('archivo', '')  
    ruta_directorio = Path(settings.BASE_DIR) / 'PresentacionesTXT'
    ruta_archivo = ruta_directorio / nombre_archivo

    try:
        if request.method == 'POST':
            titulo_presentacion = request.POST.get('tituloPresentacion', '')
            contenido_presentacion = request.POST.get('contenidoPresentacion', '')

            # Verificar si tanto el título como el contenido están presentes
            if titulo_presentacion and contenido_presentacion:
                # Verificar si el archivo existe antes de intentar guardarlo
                if os.path.exists(ruta_archivo):
                    # Sobrescribir el archivo con el nuevo título y contenido
                    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                        archivo.write(contenido_presentacion)

                    # Renombrar el archivo si el título ha cambiado
                    nuevo_nombre = ruta_directorio / (titulo_presentacion + '.txt')
                    if nuevo_nombre != ruta_archivo:
                        os.rename(ruta_archivo, nuevo_nombre)

                    return redirect('lista_presentaciones')
                else:
                    return HttpResponse("El archivo no existe.")
            else:
                return HttpResponse("El título y el contenido de la presentación son necesarios.")

        elif request.method == 'GET':
            if os.path.exists(ruta_archivo):
                with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read()
                titulo = os.path.splitext(nombre_archivo)[0]
            else:
                contenido = ""
                titulo = ""

            return render(request, 'editar_presentacion.html', {'nombre_archivo': nombre_archivo, 'contenido': contenido, 'titulo': titulo})
    except (FileNotFoundError, PermissionError) as e:
        return HttpResponse(f"Error: {e}")

def ver_presentacion(request):
    if 'archivo' in request.GET:
        nombre_archivo = request.GET['archivo']
        directorio = 'PresentacionesTXT'
        ruta_archivo = os.path.join(directorio, nombre_archivo)

        contenido_archivo = ""
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'r') as archivo:
                contenido_archivo = archivo.read()
        
        return render(request, 'ver_presentacion.html', {'nombre_archivo': nombre_archivo, 'contenido_archivo': contenido_archivo})
    else:
        return HttpResponse("No se proporcionó un archivo para visualizar.")

def procesar_contenido(archivo):
    with open(archivo, 'r') as f:
        contenido = f.read()

    # Dividir el contenido en líneas
    lineas = contenido.split('\n')

    titulos = []
    parrafos = []
    diapositivas = []

    for linea in lineas:
        linea = linea.strip()

        if linea.startswith('#'):
            # Es un título principal
            titulos.append(linea.lstrip('#').strip())  # Elimina el '#' y añade el título sin espacios al inicio y final
        elif linea.startswith('%'):
            # Es un párrafo
            parrafos.append(linea.lstrip('%').strip())  # Elimina el '%' y añade el párrafo sin espacios al inicio y final
        elif linea.startswith('--'):
            # Es una señal de salto de diapositiva
            diapositivas.append(True)

    return titulos, parrafos, diapositivas

def vista_presentacion(request):
    archivo = 'contenido.txt'
    titulos, parrafos, diapositivas = procesar_contenido(archivo)

    # Pasar los datos procesados al template
    return render(request, 'presentacion.html', {'titulos': titulos, 'parrafos': parrafos, 'diapositivas': diapositivas})