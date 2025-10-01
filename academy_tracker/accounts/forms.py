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
class PendingUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = PendingUser
        fields = ["name", "email", "semester", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user 


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser 
        fields = ["name", "email", "semester"]
        
# forms.py :
