from django.contrib import admin
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cognome', 'email', 'username', 'età', 'peso', 'altezza']


admin.site.register(CustomUser, UserAdmin)
