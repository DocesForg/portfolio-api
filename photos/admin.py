
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Импортируем модель, которую вы хотите управлять через админку
from .models import Photo, Like
from .models import UserProfile

# Зарегистрируйте модель в админке, чтобы можно было управлять фотографиями через админку Django
# Теперь вы можете управлять фотографиями через админку Django
# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/

class LikeInline(admin.TabularInline):
    model = Like
    extra = 0
    readonly_fields = ('ip_address', 'created_at')

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'user', 'likes_count')
    inlines = [LikeInline]

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('photo', 'ip_address', 'created_at')
    list_filter = ('photo', 'ip_address')
    search_fields = ('ip_address',)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

# Расширьте стандартную админку пользователя
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Регистрируем модель UserProfile (опционально)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

