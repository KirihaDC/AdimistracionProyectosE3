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
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import PasswordResetForm, PasswordResetConfirmForm
from django.contrib.auth import get_user_model

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


User = get_user_model()
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            # Verificar si el nombre de usuario y el correo electrónico coinciden
            try:
                user = User.objects.get(username=username, email=email)
            except User.DoesNotExist:
                user = None
            
            if user:
                # Si coinciden, redirigir a la página de cambio de contraseña
                return redirect('change_password', user_id=user.id)  # Pasar el user_id
            else:
                messages.error(request, 'El nombre de usuario y el correo electrónico no coinciden.')
    else:
        form = PasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})


def change_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = PasswordResetConfirmForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('homepage')
    else:
        form = PasswordResetConfirmForm(user)
    return render(request, 'change_password.html', {'form': form})

def lista_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})

def cerrar_sesion(request):
    logout(request)
    # Redirigir al usuario a alguna página después de cerrar sesión
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


def perfil(request):
    if request.method == 'POST':
        # Obtener el usuario actual
        user = request.user
        # Obtener el nuevo nombre de usuario del formulario
        new_username = request.POST.get('username')
        # Obtener las nuevas contraseñas del formulario
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')

        # Verificar si el nuevo nombre de usuario no está vacío y no es igual al nombre de usuario actual
        if new_username and new_username != user.username:
            user.username = new_username
            user.save()
            messages.success(request, 'Nombre de usuario actualizado exitosamente')

        # Verificar si las nuevas contraseñas no están vacías y son iguales
        if new_password1 and new_password1 == new_password2:
            user.set_password(new_password1)
            user.save()
            # Mantener la sesión autenticada después de cambiar la contraseña
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada exitosamente')
        elif new_password1 or new_password2:
            messages.error(request, 'Las contraseñas no coinciden')

        # Redirigir a la misma página para evitar problemas de recarga de formularios
        return redirect('perfil')

    # Si la solicitud no es POST, simplemente renderiza la página de perfil
    return render(request, 'perfil.html')
