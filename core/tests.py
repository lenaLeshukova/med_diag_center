from django.test import TestCase
from django.urls import reverse
from .models import Feedback

class CoreViewsTestCase(TestCase):
    def test_index_page_status_code(self):
        """Проверка доступности главной страницы."""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_about_page_status_code(self):
        """Проверка доступности страницы 'О компании'."""
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)

    def test_feedback_form_submission(self):
        """Проверка отправки формы обратной связи."""
        data = {
            'name': 'Тест Тестович',
            'email': 'test@example.com',
            'phone': '+79991112233',
            'message': 'Привет, это тестовое сообщение!'
        }
        response = self.client.post(reverse('core:index'), data=data)
        # После успешной отправки должен быть редирект
        self.assertEqual(response.status_code, 302)
        # Проверяем, что объект создался в БД
        self.assertEqual(Feedback.objects.count(), 1)
