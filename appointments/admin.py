from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Appointment, DiagnosticResult

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'last_name', 'first_name', 'phone', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('phone', 'medical_card_number')}),
     )

class DiagnosticResultInline(admin.StackedInline):
    model = DiagnosticResult
    extra = 1

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'service', 'date_time', 'status')
    list_filter = ('status', 'date_time', 'doctor')
    search_fields = ('patient__last_name', 'patient__first_name', 'doctor__full_name')
    inlines = [DiagnosticResultInline]
