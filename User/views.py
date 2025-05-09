from django.contrib.auth import login, logout,authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Redirect based on user role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid user role')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'auth/profile.html', {'user': request.user})