from django import forms
from .models import CustomUser


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



class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser 
        fields = ["name", "email", "semester"]
        