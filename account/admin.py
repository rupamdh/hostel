from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('phone', 'first_name', 'last_name')
    search_fields = ('phone', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

admin.site.register(User, UserAdmin)