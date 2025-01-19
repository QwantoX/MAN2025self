from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Важливо: якщо ви використовуєте email для входу, потрібно переконатися,
        # що ви правильно налаштували AUTH_USER_MODEL або використовуєте правильне поле для автентифікації
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('index')  # переконайтеся, що у вас є URL з ім'ям 'index'
        else:
            messages.error(request, 'Invalid email or password!')
    
    return render(request, 'login.html')  # змініть на правильний шлях до вашого шаблону

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Successfully logged out!')
    return redirect('login')

@login_required
def index(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')
