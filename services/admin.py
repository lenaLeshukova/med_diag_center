from django.contrib import admin
from .models import Doctor, ServiceCategory, MedicalService


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialization", "experience")
    search_fields = ("full_name", "specialization")


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(MedicalService)
class MedicalServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "duration_minutes")
    list_filter = ("category",)
    search_fields = ("name", "description")
