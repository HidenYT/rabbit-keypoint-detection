from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                User.objects.create_user(form_data['email'], form_data['email'], form_data['password'])
            except Exception as e:
                pass
            else:
                return redirect("index")
    return render(request, 'auth/register.html', {'form': form})

def login_view(request): 
    if request.user.is_authenticated:
        return redirect("index")
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form_data = form.cleaned_data
            user = authenticate(username=form_data["email"], password=form_data["password"])
            if user is not None:
                login(request, user)
                return redirect("index")
    return render(request, 'auth/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("index")