from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone

from services.models import MedicalService, Doctor
from .models import Appointment, CustomUser


class PatientRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True, label="Номер телефона",
                            widget=forms.TextInput(attrs={'placeholder': '+7 (999) 999-99-99'}))
    first_name = forms.CharField(max_length=30, required=True, label="Имя")
    last_name = forms.CharField(max_length=150, required=True, label="Фамилия")
    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('last_name', 'first_name', 'email', 'phone')

class PatientLoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'placeholder': 'Введите логин'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))


class AppointmentForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=MedicalService.objects.all(), label="Выберите услугу",
                                     empty_label="-- Не выбрано --")
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), label="Выберите специалиста",
                                    empty_label="-- Не выбрано --")
    date_time = forms.DateTimeField(
        label="Дата и время приема",
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        help_text="Выберите удобный день и доступное время"
    )

    class Meta:
        model = Appointment
        fields = ['service', 'doctor', 'date_time']

    # ВАЛИДАЦИЯ ДАТЫ:
    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')

        # Проверяем, что дата не в прошлом
        if date_time and date_time < timezone.now():
            raise forms.ValidationError("Нельзя записаться на прошедшую дату или время!")

        # Ограничиваем запись слишком далеко в будущее (например, максимум на 1 год вперед)
        if date_time and date_time.year > timezone.now().year + 1:
            raise forms.ValidationError("Запись возможна максимум на один год вперед!")

        return date_time
