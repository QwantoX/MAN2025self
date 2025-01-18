from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'role', 'is_active', 'is_staff']
    search_fields = ['email', 'username']
    list_filter = ['role', 'is_active', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
