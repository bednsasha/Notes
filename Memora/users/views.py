from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy

from main.models import ApplicantProfile
from .forms import LoginUserForm, RegisterUserForm

# Create your views here.

class LoginUser(LoginView):
    form_class=LoginUserForm
    template_name='authorization.html'
    
    
    def get_success_url(self):
        return reverse_lazy('home')

def registration(request):
    if request.method=='POST':
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            ApplicantProfile.objects.create(user=user, name=user.username, email=user.email)
            return redirect('users:login')
       # редирект или другой ответ
        else:
            return render(request, 'registration.html', {'form': form})
        
        
        
        
        
        
    else:
        form=RegisterUserForm()
    return render(request, 'registration.html',{'form':form})

def password_change(request):
    return render(request, 'password_change.html')