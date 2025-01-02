from .models import User, OTP
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["full_name", "phone", "email", "date_joined", "last_login", "is_admin"]
    readonly_fields = ["date_joined", "last_login"]
    list_filter = ["is_admin", "date_joined", "last_login"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["full_name", "phone", "bio", "image", "date_joined", "last_login"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [(None, {"classes": ["wide"], "fields": ["email", "full_name", "phone", "password1", "password2"]}),]
    search_fields = ["email", "full_name", "phone"]
    ordering = ["email"]
    filter_horizontal = []


@admin.register(OTP)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'is_expired']


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
