from rest_framework import serializers
from .models import Photo
from .models import UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'avatar']

    def get_avatar(self, obj):
        if obj.avatar:
            return self.context['request'].build_absolute_uri(obj.avatar.url)
        return None

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор для добавления имени и фамилии в JWT-ответ.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Безопасное получение профиля
        profile = getattr(user, 'profile', None)
        avatar_url = profile.avatar.url if profile and profile.avatar else None

        # Добавляем дополнительные поля в токен
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['avatar'] = avatar_url
        token['id'] = user.id

        return token

    def validate(self, attrs):
        # Получаем стандартные данные токена
        data = super().validate(attrs)

        profile = getattr(self.user, 'profile', None)
        avatar_url = profile.avatar.url if profile and profile.avatar else None

        # Добавляем имя и фамилию в ответ
        data['username'] = self.user.username
        data['first_name'] = self.user.first_name
        data['last_name'] = self.user.last_name
        data['avatar'] = avatar_url
        data['id'] = self.user.id

        return data


# это нужно для сериализации данных из бд и их отображения в виде json
# (для того, чтобы в браузере можно было увидеть данные, которые мы получаем из бд)

# тут можно создать любые дополнительные поля, которые будут отображаться в браузере
class PhotoSerializer(serializers.ModelSerializer):

    # поле для подсчета лайков 
    likes_count = serializers.SerializerMethodField()

    # поле для проверки, лайкнул ли пользователь эту фотографию
    is_liked_by_ip = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ['id', 'image', 'description', 'created_at', 'user_id', 'category_id', 'likes_count', 'is_liked_by_ip']
        read_only_fields = ['user']

    # мы должны создать функцию для подсчета лайков, потому что мы не можем использовать поле в модели (не так просто) 
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked_by_ip(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        ip = request.META.get('REMOTE_ADDR')
        return obj.likes.filter(ip_address=ip).exists()