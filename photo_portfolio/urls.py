"""
URL configuration for photo_portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# ВСЕ URL которые есть в КОРНЕ проекта
# Например, если нужно будет создать страницу для авторизации пользователя, то нужно будет создать приложение для авторизации, и затем создать URL для авторизации в этом приложении
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('photos.urls')),

    # Добавление URL для авторизации пользователя
    # Для авторизации пользователя будет использоваться JWT токен
    # JWT это тип токена, который будет использоваться для авторизации пользователя
    # JWT (JSON Web Token) — это открытый стандартизированный способ безопасной передачи информации между двумя сторонами в виде токена.
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # создание JWT токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # обновление JWT токена
]


# Добавление медиа файлов в URL
# находится в файле settings.py в переменной MEDIA_URL и MEDIA_ROOT
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)