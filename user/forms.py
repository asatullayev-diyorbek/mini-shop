from django import forms
from user.models import User
import re
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label='Username', max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control',
                'id': 'username'
            }
        )
    )
    email = forms.EmailField(
        label='Email', required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Emial',
                'class': 'form-control',
                'id': 'email'
            }
        )
    )
    password1 = forms.CharField(
        label='Make password', required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'id': 'password1'
            }
        )
    )
    password2 = forms.CharField(
        label='Make password', required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'id': 'password1'
            }
        )
    )
    phone = forms.CharField(label='Phone number', max_length=15, required=False)
    address = forms.CharField(label='Address', max_length=150, required=False)
    image = forms.ImageField(label='Profile picture', required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords must match')
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address already exists')
        if (not email.endswith('@gmail.com')) and (not email.endswith('@mail.ru')) and (not email.endswith('@yandex.com')):
            raise forms.ValidationError('Email must be from gmail.com, yandex.com or mail.ru')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        if len(username) < 5:
            raise forms.ValidationError('Username must be at least 5 characters long')
        return username

    def create_user(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'address', 'image')


class LoginForm(forms.ModelForm):
    username = forms.CharField(
        label='Username', max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'class': 'form-control',
                'id': 'username'
            }
        )
    )
    password = forms.CharField(
        label='Password', required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control',
                'id': 'password1'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username does not exist')
        user = User.objects.get(username=username)
        if not user.check_password(password):
            raise forms.ValidationError('Incorrect password')
        self.cleaned_data['user'] = self.get_user()
        return self.cleaned_data

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Amaldagi parol",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-2',
                'id': 'current_password'
            }
        )
    )
    new_password = forms.CharField(
        label="Yangi parol",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-2',
                'id': 'new_password'
            }
        )
    )
    confirm_new_password = forms.CharField(
        label="Yangi parolni qayta kiriting",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-2',
                'id': 'confirm_new_password'
            }
        )
    )

    def __init__(
            self,
            data=None,
            files=None,
            auto_id="id_%s",
            prefix=None,
            initial=None,
            error_class=ErrorList,
            label_suffix=None,
            empty_permitted=False,
            field_order=None,
            use_required_attribute=None,
            renderer=None,
    ):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
                         use_required_attribute, renderer)
        self.user = None

    def set_user(self, user):
        assert isinstance(user, User)
        self.user = user

    def clean_current_password(self):
        user = self.user
        current_password = self.cleaned_data['current_password']
        if not user.check_password(current_password):
            raise ValidationError("Amaldagi parolga to'g'ri kelmadi!")
        return current_password

    def clean_new_password(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")

        if new_password and len(new_password) < 8:
            raise ValidationError("Parolda uzunligi kamida 8ta belgi bo'lishi kerak")
        return new_password

    def clean_confirm_new_password(self):
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        new_password = self.cleaned_data.get('new_password')
        if confirm_new_password != new_password:
            raise ValidationError("Yangi parollar mos kelmadi.")
        return confirm_new_password


class UpdateProfileForm(forms.ModelForm):
    email = forms.CharField(
        max_length=100,
        label="Email",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=13,
        label="Telefon raqam",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=50,
        label="Ism",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        label="Familiya",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


    class Meta:
        model = User
        fields = ('email', 'phone')

    def clean_phone(self):
        phone_regex = r"^\+998([- ])?(90|91|93|94|95|98|99|33|97|71)([- ])?(\d{3})([- ])?(\d{2})([- ])?(\d{2})$"
        phone = self.cleaned_data['phone']
        if not re.fullmatch(phone_regex, phone) and phone:
            raise ValidationError("Telefon raqami talabga mos emas!")
        if phone and phone in [user.phone for user in User.objects.all()]:
            raise ValidationError("Bu telefon raqam allaqachon mavjud!")
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        allowed_domains = ['gmail.com', 'mail.ru', 'yandex.ru']
        domain = email.split('@')[-1]
        if domain not in allowed_domains and email:
            raise ValidationError(f"Email quyidagi formatlarda bo'lishi mumkin: {', '.join(allowed_domains)}")
        if email and email in [user.email for user in User.objects.all()]:
            raise ValidationError("Bu email allaqachon mavjud!")
        return email

