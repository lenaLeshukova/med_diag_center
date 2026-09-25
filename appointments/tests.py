from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from appointments.models import CustomUser, Appointment
from services.models import ServiceCategory, MedicalService, Doctor


class AppointmentsTestCase(TestCase):
    def setUp(self):
        # Создаем базовые данные для тестов
        self.user = CustomUser.objects.create_user(
            username='patient1', password='password123', first_name='Иван', phone='+79991110000'
        )
        self.category = ServiceCategory.objects.create(name='Тест Категория')
        self.service = MedicalService.objects.create(
            category=self.category, name='Тест Услуга', description='Описание', price=1000
        )
        self.doctor = Doctor.objects.create(
            full_name='Доктор Докторов', specialization='Терапевт', experience=5
        )

    def test_registration(self):
        """Тест успешной регистрации пользователя."""
        data = {
            'username': 'newpatient',
            'first_name': 'Петр',
            'last_name': 'Петров',
            'email': 'petr@example.com',
            'phone': '+79995554433',
            'password': 'SuperPassword123!',
            'password_again': 'SuperPassword123!',  # Для стандартного UserCreationForm
        }
        # Учитываем, что поля пароля в форме могут называться password1 и password2
        # Передадим данные, которые устроят Django форму
        data['password1'] = data['password']
        data['password2'] = data['password']

        response = self.client.post(reverse('appointments:register'), data=data)
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        """Тест авторизации пользователя."""
        response = self.client.post(reverse('appointments:login'), {
            'username': 'patient1',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_invalid_date_appointment(self):
        """Проверка блокировки записи на прошедшую дату (1111 год)."""
        self.client.login(username='patient1', password='password123')
        past_date = timezone.make_aware(timezone.datetime(1111, 1, 1, 10, 0))

        data = {
            'service': self.service.id,
            'doctor': self.doctor.id,
            'date_time': past_date.strftime('%Y-%m-%dT%H:%M')
        }
        response = self.client.post(reverse('appointments:new_appointment'), data=data)
        # Ошибка валидации вернет форму обратно (код 200), а не сделает редирект (302)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Appointment.objects.filter(patient=self.user).exists())
