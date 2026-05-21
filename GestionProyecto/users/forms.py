from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class LoginForm(AuthenticationForm):
    pass


class RegisterForm(UserCreationForm):
    rol = forms.ChoiceField(choices=CustomUser.Role.choices, initial=CustomUser.Role.ASISTENTE)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    telefono = forms.CharField(max_length=20, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'rol', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = self.cleaned_data['rol']
        user.telefono = self.cleaned_data.get('telefono', '')
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'telefono')
