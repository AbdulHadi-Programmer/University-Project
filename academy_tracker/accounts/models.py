from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

# Using Custom User Model
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
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    SEMESTER_CHOICES = [(i, f"Semester {i}") for i in range(1, 9)]
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES, default=1)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} ({self.email}) - Semester {self.semester}"
