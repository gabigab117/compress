from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import CustomCreationForm


def signup(request):

    if request.method == "POST":
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = CustomCreationForm()
    return render(request, "accounts/signup.html", context={"form": form})


def user_login(request):
    context = {}

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("index")
        else:
            context["error"] = "email ou mot de passe non valide"

    return render(request, "accounts/login.html", context=context)


def user_logout(request):
    logout(request)
    return redirect("index")
