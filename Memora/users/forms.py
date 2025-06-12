from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Адрес электронной почты',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(
        
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        
        widget=forms.TextInput(attrs={'class': 'form-control','aria-describedby': 'emailHelp'}))
    password = forms.CharField(
        
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model=get_user_model()
        fields=['username','email','password','password2']
        
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password']
    
    def clean_email(self):
        email=self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже существует')
        return email
            
    