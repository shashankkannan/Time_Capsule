import re
from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm


class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CustomSignupForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}), required=True)

    def clean_password(self):
        password = self.cleaned_data.get('password')


        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")


        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")


        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")


        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")

        # At least one special character
        if not re.search(r"[!@#$%^&*()_+-=\[\]{}|;:'\",.<>?/~`]", password):
            raise ValidationError("Password must contain at least one special character.")

        # Return the cleaned data
        return password


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'bio', 'first_name', 'last_name', 'profilepic']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input', 'readonly': 'True'}),
            'bio': forms.Textarea(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'profilepic': forms.FileInput(attrs={'id': 'fileInput', 'style': 'display: none;', 'accept': 'image/png,image/jpg,image/jpeg,image/avif'})
        }


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-input'})
