from django.db import models


class Services(models.Model):
    """All provided services"""
    title = models.CharField(max_length=50, verbose_name='Наименование')
    cost = models.IntegerField(verbose_name='Цена')
    takes_time = models.TimeField(verbose_name='Время выполнения (минут)')
    exist = models.BooleanField(verbose_name='Действует')
    discount = models.IntegerField(blank=True, null=True, verbose_name='Скидка')
    show_on_main_page = models.BooleanField(default=False, verbose_name='Показывать на главной')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
