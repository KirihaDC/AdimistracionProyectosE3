from django.shortcuts import render
from .forms import CrearArchivoForm

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

#from django.shortcuts import render
#from .forms import CrearArchivoForm

