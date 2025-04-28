'''
Добавьте сигнал для автоматического создания профиля при создании пользователя
'''


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Создание профиля пользователя
    # Если это создание нового пользователя, создаем соответствующий профиль пользователя
    # Принимаем сигнал post_save и выполняем определенные действия после создания объекта модели
    # Принимаем параметры сигналов: отправитель (sender), экземпляр объекта (instance), флаг создания (created) и другие параметры (kwargs)
    if created and not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)