from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPVerification


# ─────────────────────────────────────────────
# Custom User Admin
# ─────────────────────────────────────────────
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # What you SEE in list view
    list_display = (
        "id",
        "email",
        "name",
        "semester",
        "is_email_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    # Filters on right side
    list_filter = (
        "is_staff",
        "is_active",
        "is_email_verified",
        "semester",
        "created_at",
    )

    # Search bar
    search_fields = ("email", "name")

    # Default ordering
    ordering = ("-created_at",)

    # Read-only fields
    readonly_fields = ("created_at", "updated_at")

    # Fields when VIEWING/EDITING a user
    fieldsets = (
        ("Basic Info", {
            "fields": ("email", "password")
        }),
        ("Personal Info", {
            "fields": ("name", "semester")
        }),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "is_email_verified")
        }),
        ("Important Dates", {
            "fields": ("last_login", "created_at", "updated_at")
        }),
    )

    # Fields when ADDING a user from admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "semester", "password1", "password2", "is_staff", "is_active"),
        }),
    )


# ─────────────────────────────────────────────
# OTP Admin (VERY IMPORTANT for debugging)
# ─────────────────────────────────────────────
@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "otp",
        "otp_type",
        "is_used",
        "created_at",
    )

    list_filter = (
        "otp_type",
        "is_used",
        "created_at",
    )

    search_fields = ("email", "otp")

    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

    # Optional: prevent editing OTP manually
    def has_change_permission(self, request, obj=None):
        return False