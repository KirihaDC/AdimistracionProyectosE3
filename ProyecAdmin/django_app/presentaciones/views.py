from django.shortcuts import render
<<<<<<< HEAD
from .models import Presentacion
from django.views.generic import ListView
from .forms import CrearArchivoForm
=======
from .forms import CrearArchivoForm
#
from django.views.generic import ListView
#
#from .models import Presentacion
>>>>>>> f0d526d08e0f76358932bd96eef1217f23af076d

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

<<<<<<< HEAD
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

=======
def presentaciones(request):
    return render(request, 'Presentaciones.html')
>>>>>>> f0d526d08e0f76358932bd96eef1217f23af076d

