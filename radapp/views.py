from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Radcheck
from django.contrib import messages

def setup_admin(request):
    if User.objects.exists():
        return redirect('login')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_superuser(username=username, password=password)
        messages.success(request, 'Admin user created! Please log in.')
        return redirect('login')
    return render(request, 'setup_admin.html')

@login_required
def dashboard(request):
    users = Radcheck.objects.all()
    return render(request, 'dashboard.html', {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        Radcheck.objects.create(username=username, value=password)
        return redirect('dashboard')
    return render(request, 'add_user.html')

@login_required
def delete_user(request, user_id):
    Radcheck.objects.filter(id=user_id).delete()
    return redirect('dashboard')
