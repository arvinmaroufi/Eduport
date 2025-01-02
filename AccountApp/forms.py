from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from AccountApp.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "is_active", "is_admin"]


class SignUpForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'exapmle@gmail.com', 'class': "form-control border-0 bg-light rounded-end ps-1"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********', 'class': "form-control border-0 bg-light rounded-end ps-1"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********', 'class': "form-control border-0 bg-light rounded-end ps-1"}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'exapmle@gmail.com', 'class': "form-control border-0 bg-light rounded-end ps-1"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********', 'class': "form-control border-0 bg-light rounded-end ps-1"}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'exapmle@gmail.com', 'class': "form-control border-0 bg-light rounded-end ps-1"}))


class CodeForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control border-0 bg-light rounded-end ps-1", 'placeholder': '*****'}))


class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control border-0 bg-light rounded-end ps-1", 'placeholder': 'password'}))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': "form-control border-0 bg-light rounded-end ps-1", 'placeholder': 'confirm password'}))

    def clean(self):
        cd = super().clean()
        password = cd['password']
        confirm_password = cd['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('کلمه عبور مطابقت ندارد')
        return cd
