from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.conf import settings

from main.models import ApplicantProfile
from .forms import LoginUserForm, PasswordChangeForm, RegisterUserForm

import random

def generate_confirmation_code():
    return str(random.randint(1000, 9999))


# Create your views here.

class LoginUser(LoginView):
    form_class=LoginUserForm
    template_name='authorization.html'
    
    
    def get_success_url(self):
        return reverse_lazy('home')

def registration(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # Деактивируем пользователя до подтверждения кода
            user.save()

            code = generate_confirmation_code()
            ApplicantProfile.objects.create(
                user=user,
                name=user.username,
                email=user.email,
                confirmation_code=code,
                code_created_at=timezone.now()
            )
            # Перенаправляем на страницу ввода кода, передавая email и код через URL
            return redirect('users:code', email=user.email)

        else:
            return render(request, 'registration.html', {'form': form})
    else:
        form = RegisterUserForm()
    return render(request, 'registration.html', {'form': form})

def code(request, email):
    profile = get_object_or_404(ApplicantProfile, email=email)
    error = None
    
    if request.method == 'POST':
        # Читаем каждое поле, очищаем и объединяем в строку
        n1 = request.POST.get('n1', '').strip()
        n2 = request.POST.get('n2', '').strip()
        n3 = request.POST.get('n3', '').strip()
        n4 = request.POST.get('n4', '').strip()

        code_entered = f"{n1}{n2}{n3}{n4}"

        # Проверяем длину кода и что все символы - цифры
        if len(code_entered) == 4 and code_entered.isdigit():
            now = timezone.now()

            if (profile.confirmation_code == code_entered and
                    profile.code_created_at and
                    now - profile.code_created_at < timedelta(minutes=10)):

                user = profile.user
                user.is_active = True
                
                user.save()

                profile.confirmation_code = ''
                profile.code_created_at = None
                profile.save()

                return redirect('users:login')
            else:
                error = 'Неверный код или время действия кода истекло.'
        else:
            error = 'Пожалуйста, введите корректный код из 4 цифр.'

    else:  # GET-запрос — отправляем письмо с кодом
        subject = 'Код подтверждения регистрации'
        message = f'Ваш код подтверждения: {profile.confirmation_code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)


    return render(request, 'code.html', {'email': email, 'error': error})
# если не используете CSRF-токен в AJAX, лучше добавить токен или убрать csrf_exempt
def resend_code(request, email):
    if request.method == 'POST':
        profile = get_object_or_404(ApplicantProfile, email=email)

        # Генерируем новый 4-значный код
        new_code = ''.join([str(random.randint(0,9)) for _ in range(4)])
        profile.confirmation_code = new_code
        profile.code_created_at = timezone.now()
        profile.save()

        subject = 'Новый код подтверждения регистрации'
        message = f'Ваш новый код подтверждения: {new_code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return JsonResponse({'success': True})
        except Exception:
            return JsonResponse({'success': False})

    return JsonResponse({'success': False})

User = get_user_model()

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['password']
           
            user = get_object_or_404(User, email=email)
            user.is_active = False
            user.set_password(new_password)
            code = generate_confirmation_code()
            profile = get_object_or_404(ApplicantProfile, email=email)
            profile.confirmation_code=code
            profile.code_created_at=timezone.now()
            profile.save()
            user.save()
            return redirect('users:code', email=user.email)  # или любой другой url после смены пароля
    else:
        form = PasswordChangeForm()
    return render(request, 'password_change.html', {'form': form})