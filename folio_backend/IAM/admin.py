from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from rules.contrib.admin import ObjectPermissionsModelAdmin

from .models import MyUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = (
            "account",
            "username",
            "email",
            "id_number",
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ("account", "username", "email", "password", "id_number", "is_active", "is_admin")

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(ObjectPermissionsModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("account", "username", "email", "id_number", "bankaccount", "budget", "id_number", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("account", "password")}),
        ("Personal info", {"fields": ("username", "id_number", "email", "bankaccount", "budget")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("account", "username", "email", "id_number", "password1", "password2"),
            },
        ),
    )
    search_fields = ("account",)
    ordering = ("account",)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
