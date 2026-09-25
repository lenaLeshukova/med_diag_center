from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FeedbackForm
from services.models import MedicalService, Doctor


def index_view(request):
    """Главная страница: описание, топ-услуги и форма."""
    # Возьмем первые 3 услуги для витрины на главной
    services = MedicalService.objects.all()[:3]

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Спасибо! Ваше обращение успешно отправлено. Мы свяжемся с вами в ближайшее время.')
            return redirect('core:index')
    else:
        form = FeedbackForm()

    context = {
        'services': services,
        'form': form
    }
    return render(request, 'core/index.html', context)


def about_view(request):
    """Страница 'О компании': история, ценности и команда врачей."""
    doctors = Doctor.objects.all()
    return render(request, 'core/about.html', {'doctors': doctors})


def contacts_view(request):
    """Страница 'Контакты' с формой обратной связи."""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше сообщение отправлено из раздела контактов!')
            return redirect('core:contacts')
    else:
        form = FeedbackForm()
    return render(request, 'core/contacts.html', {'form': form})
