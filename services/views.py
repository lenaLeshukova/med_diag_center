from django.shortcuts import render
from .models import ServiceCategory

def catalog_view(request):
    """Отображение всех категорий и связанных с ними медицинских услуг."""
    # Загружаем категории вместе с услугами, чтобы избежать лишних запросов к БД
    categories = ServiceCategory.objects.prefetch_related('services').all()
    return render(request, 'services/catalog.html', {'categories': categories})
