from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username= forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password', required=True, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        pass1 = cd['password1']
        pass2 = cd['password2']
        if pass2 != pass1:
            raise forms.ValidationError('your password isn\'t identical')
        return pass2
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('user with this email is already registered')
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', ] 

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'gender', 'date_of_birth']