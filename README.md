# Projet Docstring (Aout 2023)

## Résumé

Un compresseur d'image ou ... d'images ! (Selon si le compte est premium)
Merci Pillow

### Upload simple ...

Upload d'une image, compression de l'image.

### Mais pas que !

Mise en place d'un système d'abonnement avec Stripe.
L'utilisateur peut souscrire à un compte premium. Ainsi, il aura accès aux vues premium.
En effet, je vérifie que l'utilisateur a un abonnement actif pour accéder à certaines vues. De cette manière il peut
uploader plusieurs images d'un coup et les conserver après l'upload.

L'utilisateur a la possibilité d'annuler son abonnement Stripe à tout moment.

### Notes

- stripe listen --forward-to 127.0.0.1:8000/compressor/stripe-webhook/
- https://testdriven.io/blog/django-stripe-subscriptions/#restricting-user-access
- https://pypi.org/project/django-cleanup/  ==> Pour nettoyer les fichiers