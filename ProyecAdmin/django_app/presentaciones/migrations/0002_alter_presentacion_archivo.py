# Generated by Django 4.2.8 on 2024-03-06 14:32

from django.db import migrations, models
import presentaciones.models


class Migration(migrations.Migration):

    dependencies = [
        ('presentaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentacion',
            name='archivo',
            field=models.FileField(upload_to=presentaciones.models.ruta_archivos_txt),
        ),
    ]