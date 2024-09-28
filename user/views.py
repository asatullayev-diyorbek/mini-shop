from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages

from .forms import RegisterForm, LoginForm, UpdateProfileForm, PasswordChangeForm
from .models import User


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile_form = UpdateProfileForm(instance=request.user)
        password_form = PasswordChangeForm()
        context = {
            'profile_form': profile_form,
            'password_form': password_form,
            'title': 'Profilim',
            'page_name': 'Profile',
        }
        return render(request, 'user/profile.html', context)

    def post(self, request):
        return redirect('user:profile')


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
    def get(self, request):
        context = {
            'title': 'Parolni yangilash',
            'password_form': PasswordChangeForm(),
        }
        return render(request, 'user/password_change.html', context)
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
        return render(request, 'user/password_change.html', context)


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'profile_form': UpdateProfileForm(instance=request.user),
            'title': "Ma'lumotlarni tahrirlash",
        }
        return render(request, 'user/personal_information.html', context)

    def post(self, request):
        profile_form = UpdateProfileForm(self.request.POST, instance=request.user)

        if profile_form.is_valid():
            email = profile_form.cleaned_data['email']
            phone = profile_form.cleaned_data['phone']

            if email:
                request.user.email = email
            if phone:
                request.user.phone = phone
            request.user.first_name = profile_form.cleaned_data['first_name']
            request.user.last_name = profile_form.cleaned_data['last_name']
            request.user.address = profile_form.cleaned_data['address']
            request.user.save()
            messages.success(request, "Ma'lumotlar muvafaqqiyatli yangilandi!")
            return redirect('user:profile')

        context = {
            'profile_form': profile_form,
            'title': 'Profilim',
            'page_name': 'Profile',
        }
        return render(request, 'user/personal_information.html', context)


class Register(View):
    def get(self, request):
        context = {
            'form': RegisterForm(),
            'title': "Ro'yxatdan o'tish",
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
        }
        return render(request, 'user/register.html', context)


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('shop:home')
        context = {
            'form': LoginForm(),
            'title': 'Kirish',
        }
        return render(request, 'user/login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('shop:home')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, f"Salom {user.username} siz tizimga kirdingiz!")
            to = request.GET.get('next', 'shop:home')
            return redirect(to)
        else:
            context = {
                'form': form,
                'title': 'Kirish',
            }
            return render(request, 'user/login.html', context)


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'Siz tizimdan chiqdingiz!')
    return redirect('user:login')