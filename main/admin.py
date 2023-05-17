from django.contrib import admin
from main.models import *

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'is_superuser','is_staff', 'is_active', 'user_avatar')

# display CustomUser model
admin.site.register(CustomUser, CustomUserAdmin)