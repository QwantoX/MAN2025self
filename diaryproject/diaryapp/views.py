from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SchoolClass

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
       
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password!')
   
    return render(request, 'login.html')

@login_required
def index(request):
    school_classes = SchoolClass.objects.all() #navbar 'disabled'
    context = {
        'school_classes': school_classes
    }
    return render(request, 'index.html', context)

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Successfully logged out!')
    return redirect('login')


def logout_view(request):
    logout(request)
    return redirect('login')

