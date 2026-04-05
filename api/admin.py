from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Transaction

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'type', 'category', 'date']
    list_filter = ['type', 'category']