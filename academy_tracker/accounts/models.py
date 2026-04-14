from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
import random
import string
 
 
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, semester=1, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, semester=semester, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, email, name, semester=1, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, semester, password, **extra_fields)
 
 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    name     = models.CharField(max_length=100)
    email    = models.EmailField(unique=True)
 
    SEMESTER_CHOICES = [(i, f"Semester {i}") for i in range(1, 9)]
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES, default=1)
 
    # ── NEW: email verification ──────────────────────────────
    is_email_verified = models.BooleanField(default=False)
    # ────────────────────────────────────────────────────────
 
    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
 
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
 
    USERNAME_FIELD  = "email"
    REQUIRED_FIELDS = ["name"]
 
    objects = CustomUserManager()
 
    def __str__(self):
        return f"{self.name} ({self.email}) - Semester {self.semester}"
 
 
def generate_otp():
    """6-digit numeric OTP."""
    return ''.join(random.choices(string.digits, k=6))
 
 
class OTPVerification(models.Model):
    """Stores the OTP for a pending email verification."""
 
    OTP_TYPE_CHOICES = [
        ('register', 'Registration'),
        ('login',    'Login'),
    ]
 
    email      = models.EmailField()                          # target email
    otp        = models.CharField(max_length=6)
    otp_type   = models.CharField(max_length=10, choices=OTP_TYPE_CHOICES, default='register')
    created_at = models.DateTimeField(auto_now_add=True)
    is_used    = models.BooleanField(default=False)
 
    # Store pending registration data until OTP confirmed
    pending_name     = models.CharField(max_length=100, blank=True)
    pending_password = models.CharField(max_length=255, blank=True)  # hashed
    pending_semester = models.PositiveSmallIntegerField(default=1)
 
    class Meta:
        ordering = ['-created_at']
 
    def is_expired(self):
        """OTP expires after 10 minutes."""
        from datetime import timedelta
        return timezone.now() > self.created_at + timedelta(minutes=10)
 
    def __str__(self):
        return f"OTP for {self.email} ({self.otp_type}) — {'used' if self.is_used else 'pending'}"
