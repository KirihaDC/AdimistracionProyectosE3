from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()


class ChangeRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    new_role = forms.ChoiceField(choices=(('user', 'Usuario'), ('admin', 'Administrador')))