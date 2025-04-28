from django.apps import AppConfig

# Это автоматически создаётся, когда создается приложение

# это тот файл мы создали, чтобы сделать это приложение активным
class PhotosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photos'

    def ready(self):
        import photos.signals
