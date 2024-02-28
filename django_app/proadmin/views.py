from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

def homepage(request):
     return render(request, 'homepage.html')

def reset_password(request):
    return render(request, 'password_reset_email.html')
    
def register(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        nombre_usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        
        # Verificar si las contraseñas coinciden
        if contraseña != False:
            # Crear el usuario
            nuevo_usuario = User.objects.create_user(username=nombre_usuario, email=correo, password=contraseña)
            nuevo_usuario.save()
              # Redirigir a una página de éxito
        else:
            # Contraseñas no coinciden, manejar el error aquí
            pass  # Puedes agregar una lógica para mostrar un mensaje de error al usuario
    return render(request, 'registro.html')
    
