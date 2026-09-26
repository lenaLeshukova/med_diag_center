from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),  # Главная, О компании, Контакты
    path("services/", include("services.urls")),  # Каталог услуг
    path("account/", include("appointments.urls")),  # Личный кабинет и записи
]

# Подключаем раздачу статики и медиа-файлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
