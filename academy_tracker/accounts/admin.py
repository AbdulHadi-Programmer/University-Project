from django.contrib import admin
from .models import CustomUser, PendingUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name', "email", "semester", "is_staff", "is_superuser")


admin.site.register(PendingUser)


