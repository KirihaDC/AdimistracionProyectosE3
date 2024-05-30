from django import forms

class CrearArchivoForm(forms.Form):
    nombre_archivo = forms.CharField(label='Título', max_length=100)
    contenido = forms.CharField(label='Contenido', widget=forms.Textarea)