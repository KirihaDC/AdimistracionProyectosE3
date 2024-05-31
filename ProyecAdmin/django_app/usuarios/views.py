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
from django.conf import settings
import os

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

def administrador(request):
    return render(request, 'administrador.html')

@user_passes_test(es_admin)
def registro_usuario(request):
    if request.method == 'POST':
        correo = 'correo@prueba.com'
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

@login_required
def eliminar_perfil(request):
    if request.method == 'DELETE':
        request.user.delete() 
        return HttpResponse(status=204)  
    else:
        return HttpResponse(status=405)  

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

def registro_usuarios(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        nombre_usuario = request.POST['nombre_usuario']
        contraseña = request.POST['contraseña']
        confirmar_contraseña = request.POST['confirmar_contraseña']
        # Verificar si las contraseñas coinciden
        if contraseña != confirmar_contraseña:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('registro_usuarios')
        # Crear un nuevo usuario
        user = User.objects.create_user(username=nombre_usuario, email=correo, password=contraseña)
        user.save()
        messages.success(request, 'Usuario registrado exitosamente')
        return redirect('registro_usuarios')
    return render(request, 'registro_usuarios.html')

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
        
        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=nombre_usuario).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
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

@login_required
def perfil(request):
    user = request.user
    
    # Verificar si el usuario autenticado es un administrador
    es_admin = user.is_staff

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')
        if new_username and new_username != user.username:
            user.username = new_username
            user.save()
            messages.success(request, 'Nombre de usuario actualizado exitosamente')
        if new_password1 and new_password1 == new_password2:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada exitosamente')
        elif new_password1 or new_password2:
            messages.error(request, 'Las contraseñas no coinciden')
        return redirect('perfil')

    return render(request, 'perfil.html', {'es_admin': es_admin})

#Este ya funciona
"""def leer_archivo(request): 
    ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_archivo = os.path.join(ruta_proyecto, 'PresentacionesTXT', 'Test.txt')

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
                contenido_actual.append(f'<p>{linea}</p>')

            if not linea or len(linea.strip()) == 0:
                diapositivas.append((titulo_actual, contenido_actual))
                titulo_actual = ''
                contenido_actual = []

    if titulo_actual or contenido_actual:
        diapositivas.append((titulo_actual, contenido_actual))

    return render(request, 'archivoTexto.html', {'diapositivas': diapositivas})"""

def lista_presentacionesUsuario(request):
    # Directorio donde se encuentran los archivos de texto
    directorio = os.path.join(settings.BASE_DIR, 'PresentacionesTXT')

    # Obtener una lista de todos los archivos en el directorio
    archivos = os.listdir(directorio)

    # Pasar la lista de archivos a la plantilla
    return render(request, 'presentacionUsuario_list.html', {'archivos': archivos})

def leer_archivo(request):
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

    return render(request, 'archivoTexto.html', {'diapositivas': diapositivas})