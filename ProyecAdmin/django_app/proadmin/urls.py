from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),  # Incluir las URLs de la aplicación de usuarios
    path('', include('presentaciones.urls')),  # Incluir las URLs de la aplicación de usuarios
]