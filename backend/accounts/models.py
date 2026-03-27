from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for ShopNest.

    WHY extend AbstractUser instead of using Django's built-in User?
    AbstractUser gives us everything Django's default User has (password hashing,
    permissions, admin integration) but lets us add our own fields freely.
    If we skipped this and used the default User, adding a field later would
    require a complex, risky migration. Django explicitly recommends doing this
    at the start of every project.

    WHY make email the login field instead of username?
    E-commerce apps always identify users by email. Using a username creates
    friction — users forget it. We keep USERNAME_FIELD = 'email' and make
    username optional so the rest of Django's auth machinery still works.
    """

    email = models.EmailField(unique=True)

    # We log in with email, not username. Django's auth backend will look up
    # users by this field when checking credentials.
    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS are prompted when creating a superuser via createsuperuser.
    # username is in here so the CLI still asks for it, but it won't be used to log in.
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
