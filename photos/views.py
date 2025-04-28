from django.shortcuts import render                                 # импортируем функцию для отображения страницы
from rest_framework.decorators import action                        # импортируем функцию для работы с действиями вьюсета
from rest_framework.response import Response                        # импортируем класс для работы с ответами в формате json
from rest_framework import viewsets, status                         # импортируем класс для работы с вьюсетами и статусами ответов
from rest_framework.views import APIView                            # импортируем класс для работы с вью в формате json     
from rest_framework.parsers import MultiPartParser, FormParser      # импортируем классы для работы с файлами и формами
from rest_framework.generics import RetrieveAPIView
from .models import Photo, Like                                     # импортируем модели из приложения
from .models import UserProfile                                     # импортируем класс модели пользователя  
from .serializers import UserProfileSerializer                      # импортируем класс сериализатора для работы с данными модели
from .serializers import PhotoSerializer                            # импортируем класс сериализатора для работы с данными модели
from .permissions import ReadOnlyOrIsAuthenticatedAndInGroup        # импортируем класс разрешений для работы с вьюсетом
from .permissions import IsOwner                                    # импортируем класс разрешений для работы с вьюсетом 
from django_filters.rest_framework import DjangoFilterBackend       # импортируем класс для работы с фильтрацией
from django.db import IntegrityError                                # импортируем класс для работы с исключениями
from rest_framework.permissions import BasePermission               # импортируем класс базового разрешения для работы с вьюсетом
from rest_framework.permissions import IsAuthenticated              # импортируем класс разрешений для работы с вьюсетом
from rest_framework.permissions import AllowAny                     # импортируем класс разрешений для работы с вьюсетом
from django.shortcuts import get_object_or_404                      # импортируем функцию для работы с исключениями
from django.db.models import Count, Sum                             # импортируем классы для работы с базой данных 
from django.http import HttpRequest



class IPView(APIView):
    def get(self, request: HttpRequest):
        # Получаем IP-адрес
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return Response({'ip': ip}, status=200)

class StatisticsView(APIView):
    """
    Возвращает:
    1. Количество фотографий user1
    2. Количество фотографий user2
    3. Общее количество лайков
    """
    
    def get(self, request):
        # Замените на реальные username или ID пользователей
        user1_username = 'user1'
        user2_username = 'user2'

        try:
            # Получаем количество фото для user1
            user1_photos = Photo.objects.filter(user__username=user1_username).count()

            # Получаем количество фото для user2
            user2_photos = Photo.objects.filter(user__username=user2_username).count()

            # Общее количество лайков
            total_likes = Like.objects.count()  # Если лайки хранятся в модели Like
            # Или через аннотацию, если лайки в Photo:
            # total_likes = Photo.objects.aggregate(total_likes=Sum('likes_count')).get('total_likes', 0) or 0

            return Response({
                "user1_photos": user1_photos,
                "user2_photos": user2_photos,
                "total_likes": total_likes
            }, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    
    def get(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class UserProfileView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user__id'  # Ищем по user_id

    def get_object(self):
        user_id = self.kwargs['user_id']
        user_profile = get_object_or_404(UserProfile, user__id=user_id)
        return user_profile

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Для правильного формирования URL аватара
        return context

class IsPhotographerOrArtist(BasePermission):
    """
    Разрешение: только пользователи из групп Photographer или Artist могут создавать фото.
    """
    def has_permission(self, request, view):
        return (
            request.user.groups.filter(name='Photographer').exists() or
            request.user.groups.filter(name='Artist').exists()
        )


# это класс вьюсета, он принимает на вход класс сериализатора и класс модели, и на выходе дает нам все объекты модели и возможность их изменять через api
# т.е. мы можем посмотреть все картинки и их свойства, добавить новую картинку, удалить картинку, изменить картинку

class PhotoViewSet(viewsets.ModelViewSet):

    # queryset это все объекты модели сортированные по дате создания по убыванию 
    queryset = Photo.objects.all().order_by('-created_at')
    # класс сериализатора для работы с данными модели 
    serializer_class = PhotoSerializer

    # Делаем так, чтобы только пользователи с правами фотографа или художника могли создавать фотографии
    permission_classes = [ReadOnlyOrIsAuthenticatedAndInGroup]  # Основное разрешение для CRUD

    # Чтобы добавить лимит без изменения структуры ответа, просто фильтруйте queryset
    # т.е. можно посмотреть все фото, но если добавить к запросу ?limit=10, то будет показано только 10 последних фото
    def get_queryset(self):
        queryset = super().get_queryset()
        limit = self.request.query_params.get('limit')
        if limit:
            try:
                limit = int(limit)
                queryset = queryset[:limit]  # Просто ограничиваем queryset
            except ValueError:
                pass  # Игнорируем невалидные значения
        return queryset

    
    def get_permissions(self):
        """
        Переопределяем разрешения для метода DELETE.
        """
        if self.action == 'destroy':
            return [IsAuthenticated(), IsOwner()]  # Только владелец может удалять
        return super().get_permissions()
    
    def destroy(self, request, *args, **kwargs):
        photo = self.get_object()
        if photo.user != request.user:
            return Response(
                {"error": "Вы не можете удалить чужую фотографию."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        photo.delete()
        return Response(
            {"status": "Успех", "message": f"Фотография удалена."},
            status=status.HTTP_200_OK  # Явный ответ об успехе
        )

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        # Разрешаем анонимные запросы для метода like
        self.permission_classes = [AllowAny]
        return super().like(request, pk)

    def perform_create(self, serializer):
        """
        Автоматически привязываем фото к текущему пользователю.
        """
        serializer.save(user=self.request.user)

    # Добавляем поддержку фильтрации
    filter_backends = [DjangoFilterBackend]  
    # Разрешаем фильтрацию по полю id
    filterset_fields = ['id', 'category_id', 'user_id']  


    # Метод для добавления лайка к фотографии
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[AllowAny],  # !!! Важно указать здесь
        authentication_classes=[]        # Отключаем аутентификацию
    )
    def like(self, request, pk=None):
        photo = self.get_object()
        ip = request.META.get('REMOTE_ADDR')

        # Проверяем, уже есть ли лайк от этого IP
        like_exists = photo.likes.filter(ip_address=ip).exists()

        if like_exists:
            # Удаляем лайк
            Like.objects.filter(photo=photo, ip_address=ip).delete()
            message = "Лайк удален"
        else:
            # Добавляем лайк
            Like.objects.create(photo=photo, ip_address=ip)
            message = "Лайк добавлен"

        serializer = self.get_serializer(photo)
        return Response({
            "status": message,
            "photo": serializer.data
        }, status=status.HTTP_200_OK)