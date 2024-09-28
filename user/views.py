from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages

from .forms import RegisterForm, LoginForm, UpdateProfileForm, PasswordChangeForm
from .models import User


class ProfileView(View):
    def get(self, request):
        profile_form = UpdateProfileForm()
        password_form = PasswordChangeForm()
        context = {
            'profile_form': profile_form,
            'password_form': password_form,
            'title': 'Profilim',
            'page_name': 'Profile',
            'page_icon': 'https://www.freeiconspng.com/thumbs/user-icon/user-icon--16.png'
        }
        return render(request, 'user/profile.html', context)

    def post(self, request):
        profile_form = UpdateProfileForm(self.request.POST)

        if profile_form.is_valid():
            request.user.email = profile_form.cleaned_data['email']
            request.user.phone = profile_form.cleaned_data['phone']
            request.user.save()
            messages.success(request, "Qo'shimcha ma'lumotlar muvafaqqiyatli yangilandi!")
            return redirect('user:profile')

        context = {
            'profile_form': profile_form,
            'password_form': PasswordChangeForm(),
            'title': 'Profilim',
            'page_name': 'Profile',
            'page_icon': 'https://www.freeiconspng.com/thumbs/user-icon/user-icon--16.png'
        }
        return render(request, 'user/profile.html', context)


class UpdateProfileImageView(LoginRequiredMixin, View):
    def post(self, request):
        if 'image' in request.FILES:
            image = request.FILES['image']
            if image.name.endswith(('.jpg', '.jpeg', '.png')):
                user = request.user
                user.image = image
                user.save()
                messages.success(request, 'Profil rasmi o\'zgartirildi!')
            else:
                messages.error(request, 'Noto\'g\'ri fayl formati. JPG, JPEG yoki PNG formatidagi rasmni tanlang.')
                return redirect('user:profile')
        messages.error(request, 'Rasmni yuklashda xato!')
        return redirect('user:profile')


class PasswordChangeView(LoginRequiredMixin, View):
    def post(self, request):
        user = get_object_or_404(User, id=request.user.id)
        password_form = PasswordChangeForm(request.POST)
        password_form.set_user(self.request.user)

        if password_form.is_valid():
            new_password = password_form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Parolingiz yangilandi!")
            return redirect('user:profile')

        context = {
            'title': 'Parolni yangilash - Student Office',
            'password_form': password_form,
            'profile_form': UpdateProfileForm(),
        }
        return render(request, 'user/profile.html', context)


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