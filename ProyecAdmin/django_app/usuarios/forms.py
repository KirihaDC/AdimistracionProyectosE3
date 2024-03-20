from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()


class ChangeRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    new_role = forms.ChoiceField(choices=(('user', 'Usuario'), ('admin', 'Administrador')))


class PasswordResetForm(forms.Form):
    username = forms.CharField(label='Nombre de Usuario')
    email = forms.EmailField(label='Correo Electrónico')


class PasswordResetConfirmForm(SetPasswordForm):
    """
    Un formulario para permitir a un usuario restablecer su contraseña sin proporcionar la contraseña actual.
    """
    new_password1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmar nueva contraseña", widget=forms.PasswordInput)

    def clean_new_password2(self):
        """
        Verifica que las dos contraseñas coincidan.
        """
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2