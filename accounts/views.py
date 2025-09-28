from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # redireciona para dashboard
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "As senhas não coincidem")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Usuário já existe")
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect("login")

    return render(request, "accounts/register.html")
