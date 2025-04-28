from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotoViewSet
from .views import  UserProfileView  # добавляем маршрут для получения профиля пользователя
from .views import StatisticsView    # добавляем маршрут для получения статистики
from .views import IPView


router = DefaultRouter()

# это нужно для создания CRUD операций над фото
# CRUD = Create, Read, Update, Delete
router.register(r'photos', PhotoViewSet)

# подключаем эти маршруты к нашим урлам
urlpatterns = [
    path('', include(router.urls)),
]

# маршрут для получения профиля пользователя
urlpatterns += [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]

# маршрут для получения профиля пользователя с указанием id пользователя
urlpatterns += [
    path('user/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
]

# маршрут для получения статистики
urlpatterns += [
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]

# маршрут для получения IP адреса пользователя
urlpatterns += [
    path('ip/', IPView.as_view(), name='get-ip'),
]