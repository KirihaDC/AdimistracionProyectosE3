from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=100)

nuevo_usuario = Usuario(nombre='Juan', correo='juan@example.com', contrasena='contrasena123')
nuevo_usuario.save()

