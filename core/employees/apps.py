from django.apps import AppConfig


class Employees(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'employees'
    verbose_name = 'Сотрудники'

    def ready(self):
        """Implicitly connect a signal handlers decorated with @receiver."""
        from . import signals