from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomCreationForm
from .models import CustomUser
from project.settings import STRIPE_KEY
import stripe


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


@login_required
def profile(request):
    user = request.user

    if user.stripe_sub_id:
        stripe_api_key = STRIPE_KEY
        subscription = stripe.Subscription.retrieve(user.stripe_sub_id)
        product = stripe.Product.retrieve(subscription.plan.product)
        return render(request, 'accounts/profile.html', context={'subscription': subscription,
                                                                 'product': product})

    else:
        return render(request, "accounts/profile.html")




