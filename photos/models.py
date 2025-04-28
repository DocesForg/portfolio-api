from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'  # Явное имя связи
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

class Photo(models.Model):
    # куда будет сохраняться фото
    image = models.ImageField(upload_to='photos/')
    # комментарий к фото
    description = models.TextField(blank=True)
    # время создания фото
    created_at = models.DateTimeField(auto_now_add=True)
    # кто создал фото
    # для того чтобы можно было обращаться к пользователю через фото, нужно использовать ForeignKey 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # категория фото
    category_id = models.IntegerField(default=0)
    
    # перед сохранением модели, определяем категорию на основе группы пользователя
    #метод будет вызываться каждый раз, когда мы сохраняем модель
    # так как при сохранении модели мы не можем обращаться к группам пользователя, мы будем использовать метод save
    # и передавать ему аргументы *args и **kwargs
    def save(self, *args, **kwargs):
        # Определяем категорию на основе группы пользователя
        if self.user.groups.filter(name='Photographer').exists():
            self.category_id = 0
        elif self.user.groups.filter(name='Artist').exists():
            self.category_id = 1
        super().save(*args, **kwargs)



    
    

    # количество лайков
    @property
    def likes_count(self):
        return self.likes.all().count()
    
    # имя фото будет равно имени, которое задано при создании объекта
    def __str__(self):
        return f"Photo {self.id}"
    
# Модель лайка для фотографии 
class Like(models.Model):
    # фото к которому будет привязан лайк
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    # IP адрес пользователя, который поставил лайк
    ip_address = models.GenericIPAddressField()
    # время создания лайка
    created_at = models.DateTimeField(auto_now_add=True)

    # Мета-класс для модели Like который определяет, что каждый пользователь может поставить лайк только один раз для каждой фотографии. 
    # Это предотвращает дублирование лайков от одного и того же пользователя.
    class Meta:
        unique_together = ('photo', 'ip_address')  # Один IP = один лайк на фото
    

# При изменении этого файла нужно выполнить команду:
# python manage.py makemigrations 
# python manage.py migrate