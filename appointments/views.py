from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientRegistrationForm, PatientLoginForm, AppointmentForm
from .models import Appointment

def register_view(request):
    """Регистрация нового пациента."""
    if request.user.is_authenticated:
        return redirect('appointments:dashboard')
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать в личный кабинет.')
            return redirect('appointments:dashboard')
    else:
        form = PatientRegistrationForm()
    return render(request, 'appointments/register.html', {'form': form})

def login_view(request):
    """Авторизация пациента."""
    if request.user.is_authenticated:
        return redirect('appointments:dashboard')
    if request.method == 'POST':
        form = PatientLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Рады видеть вас снова, {user.first_name}!')
                return redirect('appointments:dashboard')
    else:
        form = PatientLoginForm()
    return render(request, 'appointments/login.html', {'form': form})

def logout_view(request):
    """Выход из системы."""
    logout(request)
    messages.info(request, 'Вы успешно вышли из личного кабинета.')
    return redirect('core:index')

@login_required(login_url='appointments:login')
def dashboard_view(request):
    """Личный кабинет: список записей пациента и их результаты."""
    # Получаем все записи текущего залогиненного пользователя
    appointments = Appointment.objects.filter(patient=request.user).select_related('service', 'doctor').prefetch_related('result')
    return render(request, 'appointments/dashboard.html', {'appointments': appointments})

@login_required(login_url='appointments:login')
def create_appointment_view(request):
    """Онлайн-запись на диагностику."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user  # Привязываем запись к текущему пользователю
            appointment.save()
            messages.success(request, 'Вы успешно записались на прием! Статус записи можно отслеживать в кабинете.')
            return redirect('appointments:dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create_appointment.html', {'form': form})
