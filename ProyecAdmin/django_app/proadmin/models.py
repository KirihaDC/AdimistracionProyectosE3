from django.db import models
from markdownx.models import MarkdownxField

class Usuario(models.Model):
    usuario = models.CharField(max_length=50)
    correo = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = MarkdownxField()


