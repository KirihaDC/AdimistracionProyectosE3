import os
from django.db import models

# Create your models here.
def ruta_archivos_txt(instance, filename):
    return os.path.join('PresentacionesTXT', filename)

class Presentacion(models.Model):
    archivo = models.FileField(upload_to=ruta_archivos_txt)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre