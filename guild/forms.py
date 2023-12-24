from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User, Group
from django.core.mail import mail_admins, EmailMultiAlternatives

from .models import Post, Response, Profile, Category


# Форма регистрации
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    def save(self, commit=True):
        user = super().save(commit)
        authors = Group.objects.get(name="authors")

        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/post/">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        if not user.groups.filter(name="authors").exists():
            user.groups.add(authors)
            authors.save()
            return user

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password1', 'password2']


class ConfirmationCodeForm(forms.Form):
    code = forms.CharField(label='Confirmation Code', max_length=10)


# Форма объявления
class PostForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']


# Форма отклика
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']


class ResponseModerationForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['is_approved']


# Форма профиля
class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField()
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Profile
        fields = ['avatar', 'first_name', 'last_name', 'bio']

    def save(self, commit=True):
        user = self.instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return super().save(commit)


class ResponseFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Выберите категорию", required=False)


# Форма изменения пароля
class UserPasswordChangeForm(SetPasswordForm):
    """
    Форма изменения пароля
    """
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })


# Форма восстановления пароля
class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите Email',
                   "autocomplete": "email"}
        )
    )


# Форма установки нового пароля для пользователя.
class CustomSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": "Пароли не совпадают"
    }
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Введите новый пароль',
                   "autocomplete": "new-password"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтверждение нового пароля',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Подтвердите новый пароль',
                   "autocomplete": "new-password"}
        ),
    )