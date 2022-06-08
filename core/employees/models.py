from datetime import time
from django.db import models
from authentication.models import User


class Employees(models.Model):
    """Model describes employees"""
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    position = models.CharField(max_length=50, verbose_name='Должность')
    photo = models.ImageField(upload_to='photo', blank=True, null=True, verbose_name='Фото')
    birthday = models.DateField(blank=True, null=True, verbose_name='Дата рождения')

    def __str__(self):
        return f'{self.user.first_name}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Schedule(models.Model):
    """Model describes master`s schedule: add work-days ad days-off"""
    master = models.ForeignKey(Employees, on_delete=models.PROTECT, verbose_name='Мастер')
    day = models.DateField(verbose_name='Рабочий день')
    start = models.TimeField(default=time(10, 0), verbose_name='Начало дня')
    end = models.TimeField(default=time(22, 0), verbose_name='Конец дня')
    is_reserved_hours = models.CharField(max_length=255, default='', verbose_name='Занятые часы')

    def __str__(self):
        return f'{self.day} '

    class Meta:
        ordering = ['day']
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class Hours(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT, verbose_name='Рабочий день')
    hour = models.TimeField(verbose_name='Час')
    booked = models.BooleanField(default=False, verbose_name='Зарезервирован')
    appointment_id = models.IntegerField(unique=True, verbose_name='ID записи')

    def __str__(self):
        return f'{self.hour} часов'

    class Meta:
        verbose_name = 'Рабочий час'
        verbose_name_plural = 'Рабочие часы'