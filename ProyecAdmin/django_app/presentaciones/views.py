from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from pathlib import Path
from django.conf import settings
import os

def crear_archivo(request):
    if request.method == 'POST':
        titulo = request.POST.get('tituloPresentacion', '')
        contenido = request.POST.get('contenidoPresentacion', '')

        try:
            directorio = os.path.join(settings.BASE_DIR, 'PresentacionesTXT')
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            
            ruta_archivo = os.path.join(directorio, f'{titulo}.txt')

            with open(ruta_archivo, 'w') as archivo:
                archivo.write(contenido)

            mensaje = 'La presentación se generó correctamente.'
            return render(request, 'Presentaciones.html', {'mensaje': mensaje})
        except Exception as e:
            mensaje = f'Error al generar el archivo: {e}'
            return render(request, 'Presentaciones.html', {'mensaje': mensaje})

    return render(request, 'Presentaciones.html')

def presentaciones(request):
    return render(request, 'Presentaciones.html')

def lista_presentaciones(request):
    directorio = os.path.join(settings.BASE_DIR, 'PresentacionesTXT')

    if not os.path.exists(directorio):
        archivos = []
    else:
        archivos = os.listdir(directorio)

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

            if titulo_presentacion and contenido_presentacion:
                if os.path.exists(ruta_archivo):
                    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                        archivo.write(contenido_presentacion)

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
                try:
                    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                        contenido = archivo.read()
                except UnicodeDecodeError:
                    with open(ruta_archivo, 'r', encoding='ISO-8859-1') as archivo:
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
                font_changed = False;
                #robarse el texto que indica la fuente
                if linea.startswith('&~ '):
                    name = linea[3:]
                    #nadamas para verificar
                    #contenido_actual.append(f'<p>{path}</p>')
                    contenido_actual.append(f'<font face="{name}">')
                    font_changed = True;
                else:
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
                        if (font_changed == True):
                            contenido_actual.append(f'</font>')
                        else:
                            diapositivas.append((titulo_actual, contenido_actual))
                            titulo_actual = ''
                            contenido_actual = []

            if titulo_actual or contenido_actual:
                diapositivas.append((titulo_actual, contenido_actual))

        return render(request, 'ver_presentacion.html', {'diapositivas': diapositivas})
    
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        
        # Leer el contenido del archivo
        with open(fs.path(filename), 'r') as f:
            file_content = f.read()
        
        return render(request, 'archivoTexto.html', {
            'uploaded_file_url': uploaded_file_url,
            'file_content': file_content
        })
    return render(request, 'archivoTexto.html')


