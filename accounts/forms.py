# Django packages
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
# Third party apps
from ckeditor.widgets import CKEditorWidget
# Local apps
from .models import User


# User model customize
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'fullname', 'bio', 'age')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="You can change password using <a href=\"../password/\">this form</a>"
    )

    class Meta:
        model = User
        fields = (
            'phone_number',
            'email',
            'fullname',
            'bio',
            'age',
            'password',
            'is_active',
            'is_admin'
        )


# User authentication
class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'شماره تماس'}
    ))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': 'پست الکترونیکی'}
    ))
    fullname = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'نام کامل'}
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input', 'placeholder': 'گزرواژه'}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input', 'placeholder': 'تایید گزرواژه'}
    ))

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        user = User.objects.filter(phone_number=phone_number)
        if user:
            raise ValidationError('This phone number already exists!')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError('This email address already exists')
        return email


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'شماره تماس'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'password-input', 'placeholder': 'گزرواژه'}
    ))


class UserEditProfileForm(forms.Form):
    phone_number = forms.CharField(max_length=11, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'شماره تماس'}
    ))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(
        attrs={'class': 'email-input', 'placeholder': 'پست الکترونیکی'}
    ))
    fullname = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'email-input', 'placeholder': 'نام کامل'}
    ))
    age = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'email-input', 'placeholder': 'سن'}
    ))
    bio = forms.CharField(widget=CKEditorWidget(
        attrs={'class': 'form-control'}
    ))
    image = forms.ImageField()
