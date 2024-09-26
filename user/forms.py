from django import forms

from user.models import User


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
