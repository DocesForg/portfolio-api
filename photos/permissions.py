from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    """
    Разрешение: только владелец фотографии может её удалять.
    """
    message = "Вы не являетесь владельцем этой фотографии."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class ReadOnlyOrIsAuthenticatedAndInGroup(BasePermission):
    """
    Разрешение:
    - Чтение (GET, HEAD, OPTIONS) доступно всем.
    - Запись (POST, PUT, DELETE) доступна только авторизованным пользователям из групп Photographer/Artist.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True

        # Для записи проверяем аутентификацию и принадлежность к группам
        return (
            request.user.is_authenticated and
            (request.user.groups.filter(name='Photographer').exists() or
             request.user.groups.filter(name='Artist').exists())
        )