from django.conf import settings
from services.models import MedicalService, Doctor
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, verbose_name="Номер телефона", blank=True, null=True)
    medical_card_number = models.CharField(max_length=50, verbose_name="Номер мед. карты", blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.username})"

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('confirmed', 'Подтверждена'),
        ('completed', 'Выполнена'),
        ('canceled', 'Отменена'),
    ]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments', verbose_name="Пациент")
    service = models.ForeignKey(MedicalService, on_delete=models.CASCADE, related_name='appointments', verbose_name="Услуга")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name="Врач")
    date_time = models.DateTimeField(verbose_name="Дата и время приема")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="Статус записи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"
        ordering = ['-date_time']

    def __str__(self):
        return f"Запись #{self.id}: {self.patient.last_name} к {self.doctor.full_name} ({self.date_time})"

class DiagnosticResult(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='result', verbose_name="Запись на прием")
    conclusion = models.TextField(verbose_name="Медицинское заключение")
    pdf_report = models.FileField(upload_to='results/', verbose_name="Файл результатов (PDF)", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Результат диагностики"
        verbose_name_plural = "Результаты диагностики"

    def __str__(self):
        return f"Результат для записи #{self.appointment.id}"
