import stripe
from django.contrib import messages
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password):
        if not email:
            raise ValueError("Email obligatoire")

        user = self.model(email=self.normalize_email(email=email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        return user


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    stripe_id = models.CharField(max_length=200, blank=True)
    stripe_sub_id = models.CharField(max_length=200, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = CustomUserManager()

    def cancel_stripe_subscription(self, request):
        stripe.Subscription.delete(self.stripe_sub_id)
        messages.add_message(request, messages.INFO, "Votre abonnement a bien été annulé")
