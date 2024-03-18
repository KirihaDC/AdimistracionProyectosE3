from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .forms import ChangeRoleForm
from django.views.decorators.http import require_POST
from django.contrib.auth import logout


def es_admin(user):
    return user.is_superuser


def homepage(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        contraseña = request.POST.get('contraseña')
        usuario = authenticate(username=nombre_usuario, password=contraseña)
        if usuario is not None:
            login(request, usuario)
            if usuario.is_superuser:  # Verifica si el usuario es administrador
                return redirect('administrador')  # Redirige a la vista del administrador
            else:
                return redirect('inicio')  # Redirige a la vista del usuario normal
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'homepage.html')

def inicio(request):
    return render(request, 'inicio.html')

@user_passes_test(es_admin)
def administrador(request):
    return render(request, 'administrador.html')


def reset_password(request):
    return render(request, 'reset_password.html')

def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def cerrar_sesion(request):
    logout(request)
    # Redirigir al usuario a alguna página después de cerrar sesión
    return redirect('homepage')

def logout_view(request):
    logout(request)
    return redirect('homepage')

@user_passes_test(es_admin)
@require_POST
def cambiar_rol(request, usuario_id):
    if request.method == 'POST':
        nuevo_rol = request.POST.get('nuevo_rol')
        if nuevo_rol in ['admin', 'user']:
            usuario = User.objects.get(pk=usuario_id)
            usuario.is_superuser = (nuevo_rol == 'admin')
            usuario.save()
    return redirect('lista_usuarios')

@user_passes_test(es_admin)
@login_required
@permission_required('auth.delete_user', raise_exception=True)
def eliminar_cuenta(request, usuario_id):
    if request.user.is_superuser:
        usuario = User.objects.get(pk=usuario_id)
        usuario.delete()
        return redirect('lista_usuarios') 
    else:
        return render({'mensaje': 'El usuario no existe'}, status=400)

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

@user_passes_test(es_admin)
def presentaciones(request):
    return render(request, 'presentaciones.html')
    