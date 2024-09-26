from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from .forms import RegisterForm, LoginForm


class Register(View):
    def get(self, request):
        context = {
            'form': RegisterForm(),
            'title': "Ro'yxatdan o'tish",
            'page_name': "Register",
            'page_icon': "https://static.vecteezy.com/system/resources/thumbnails/010/695/423/small_2x/fill-out-the-e-mail-form-with-a-pen-vector.jpg"
        }
        return render(request, 'user/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.create_user()
            messages.success(request, "Ro'yxatdan o'tdingiz! Tizimga kirish uchun login qilishni unutmaslik qoldi.")
            return redirect('user:login')
        context = {
            'form': form,
            'title': "Ro'yxatdan o'tish",
            'page_name': "Register",
            'page_icon': "https://static.vecteezy.com/system/resources/thumbnails/010/695/423/small_2x/fill-out-the-e-mail-form-with-a-pen-vector.jpg"
        }
        return render(request, 'user/register.html', context)


class Login(View):
    def get(self, request):
        context = {
            'form': LoginForm(),
            'title': 'Kirish',
            'page_name': 'Login',
            'page_icon': 'https://www.freeiconspng.com/thumbs/login-icon/door-login-icon--1.png'
        }
        return render(request, 'user/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f"Salom {user.username} siz tizimga kirdingiz!")
            return redirect('shop:home')
        else:
            context = {
                'form': form,
                'title': 'Kirish',
                'page_name': 'Login',
                'page_icon': 'https://www.freeiconspng.com/thumbs/login-icon/door-login-icon--1.png'
            }
            return render(request, 'user/login.html', context)


def logout_user(request):
    logout(request)
    messages.warning(request, 'Siz tizimdan chiqdingiz!')
    return redirect('user:login')