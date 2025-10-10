from django import forms
from .models import CustomUser, PendingUser
from django.contrib.auth.hashers import make_password


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["name", "email", "semester", "password"]

    # override save to handle password hashing
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# Pending User Form :    
from django import forms
from django.contrib.auth.hashers import make_password
from .models import PendingUser, CustomUser

class PendingUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = PendingUser
        fields = ["name", "email", "semester", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        # Check if email already exists in pending users
        if PendingUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A pending account with this email already exists. Please check your inbox."
            )

        # Also check if it's already verified (in CustomUser)
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists. Please log in."
            )

        return email

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data["password"])
        if commit:
            instance.save()
        return instance


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser 
        fields = ["name", "email", "semester"]
        
# forms.py :
