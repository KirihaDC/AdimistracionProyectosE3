from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserRegistrationForm

def homepage(request):
     return render(request, 'homepage.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirige a la página que desees
            return redirect('registro.html')  # Cambia 'pagina_exito' por el nombre de la URL de la página de éxito
    else:
        form = UserRegistrationForm()
    return render(request, 'registro.html', {'form': form})

def reset_password(request):
    return render(request, 'password_reset_email.html')
    
    
