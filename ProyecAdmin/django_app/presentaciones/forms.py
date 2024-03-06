from django import forms

class CrearArchivoForm(forms.Form):
    nombre_archivo = forms.CharField(max_length=100)
    contenido = forms.CharField(widget=forms.Textarea)