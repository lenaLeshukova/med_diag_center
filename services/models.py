from django.db import models

class Doctor(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="ФИО Врача")
    specialization = models.CharField(max_length=100, verbose_name="Специализация")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы (лет)")
    photo = models.ImageField(upload_to='doctors/', verbose_name="Фотография", blank=True, null=True)
    bio = models.TextField(verbose_name="О враче / Биография", blank=True)

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"

    def __str__(self):
        return f"{self.full_name} ({self.specialization})"

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории", blank=True)

    class Meta:
        verbose_name = "Категория услуг"
        verbose_name_plural = "Категории услуг"

    def __str__(self):
        return self.name

class MedicalService(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services', verbose_name="Категория")
    name = models.CharField(max_length=150, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Подробное описание услуги")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (руб.)")
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность (мин)", default=30)

    class Meta:
        verbose_name = "Медицинская услуга"
        verbose_name_plural = "Медицинские услуги"

    def __str__(self):
        return f"{self.name} — {self.price} руб."
