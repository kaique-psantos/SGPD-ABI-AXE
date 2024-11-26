from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .forms import FormularioCriarUser

#UsuarioCustomizado
class UsuarioCustomizado(UserAdmin):
    add_form = FormularioCriarUser
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'pessoa'),
        }),
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'email'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

admin.site.unregister(User)
admin.site.register(User, UsuarioCustomizado)