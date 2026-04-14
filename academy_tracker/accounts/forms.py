from django import forms
from .models import CustomUser
 
 
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
 
    class Meta:
        model  = CustomUser
        fields = ["name", "email", "semester", "password"]
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
 
 
class LoginForm(forms.Form):
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
 
 
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model  = CustomUser
        fields = ["name", "email", "semester"]
 
 
class OTPVerifyForm(forms.Form):
    """6 individual digit inputs — joined before validation."""
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'maxlength': '6', 'autocomplete': 'one-time-code'}),
        error_messages={
            'min_length': 'OTP must be exactly 6 digits.',
            'max_length': 'OTP must be exactly 6 digits.',
            'required':   'Please enter the OTP.',
        }
    )
 
    def clean_otp(self):
        otp = self.cleaned_data.get('otp', '').strip()
        if not otp.isdigit():
            raise forms.ValidationError("OTP must contain only numbers.")
        return otp
