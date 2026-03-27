from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Extend Django's built-in UserAdmin so password hashing UI still works
    ordering = ('email',)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
