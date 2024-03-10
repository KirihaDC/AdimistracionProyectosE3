from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login

def homepage(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        contraseña = request.POST.get('contraseña')
        usuario = authenticate(username=nombre_usuario, password=contraseña)
        if usuario is not None:
            login(request, usuario)
            if usuario.is_staff:  # Verifica si el usuario es administrador
                return redirect('administrador')  # Redirige a la vista del administrador
            else:
                return redirect('inicio')  # Redirige a la vista del usuario normal
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'homepage.html')

def inicio(request):
    return render(request, 'inicio.html')

@staff_member_required
def administrador(request):
    return render(request, 'administrador.html')


def reset_password(request):
    return render(request, 'reset_password.html')

def help(request):
    return render(request, 'help.html')
    
def register(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        nombre_usuario = request.POST['nombre_usuario']
        contraseña = request.POST['contraseña']
        confirmar_contraseña = request.POST['confirmar_contraseña']
        # Verificar si las contraseñas coinciden
        if contraseña != confirmar_contraseña:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('registro')
        # Crear un nuevo usuario
        user = User.objects.create_user(username=nombre_usuario, email=correo, password=contraseña)
        user.save()
        messages.success(request, 'Usuario registrado exitosamente')
        return redirect('homepage')
    return render(request, 'registro.html')
