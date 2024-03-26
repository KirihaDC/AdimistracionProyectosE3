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
        ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_archivo = os.path.join(ruta_proyecto, 'PresentacionesTXT', nombre_archivo)

        diapositivas = []
        titulo_actual = ''
        contenido_actual = []
        numero_pagina = 1

        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()

                if linea.startswith('<Titulo>') and linea.endswith('</Titulo>'):
                    titulo_actual = f'<strong style="font-size: larger;">{linea[8:-9]}</strong>'  # Quitar etiquetas <Titulo> y </Titulo>
                    titulo_actual += f'<span style="float: right; font-size: smaller;">Página {numero_pagina}</span>'
                    numero_pagina += 1
                else:
                    # Buscar y reemplazar las etiquetas de color con el código CSS correspondiente
                    colores = {
                        'Red': 'color: red;',
                        'Blue': 'color: blue;',
                        'Green': 'color: green;',
                        'Yllw': 'color: yellow;',
                        'Black': 'color: black;',
                        'Orge': 'color: orange;',
                        'Brwn': 'color: brown;'
                    }
                    for color, style in colores.items():
                        linea = linea.replace(f'<{color}>', f'<span style="{style}">').replace(f'</{color}>', '</span>')

                    contenido_actual.append(f'<p>{linea}</p>')

                if not linea or len(linea.strip()) == 0:
                    diapositivas.append((titulo_actual, contenido_actual))
                    titulo_actual = ''
                    contenido_actual = []

        if titulo_actual or contenido_actual:
            diapositivas.append((titulo_actual, contenido_actual))

        return render(request, 'archivoTexto.html', {'diapositivas': diapositivas})