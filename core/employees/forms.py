from datetime import date
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Schedule


class EmployeeLogingForm(AuthenticationForm):
    """Master login form"""
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )

    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control'}

        ),
    )


class AddScheduleForm(forms.Form):
    """Date picker form"""
    today = date.today().strftime('%Y-%m-%d')
    start = forms.CharField(
        initial=today,
        widget=forms.DateInput(attrs={
            'class': 'form-control ml-1',
            'type': 'date',
            'id': 'start',
            'min': today,
        })
    )

    end = forms.CharField(
        widget=forms.DateInput(attrs={
            'class': 'form-control ml-1',
            'type': 'date',
            'id': 'end',
            'min': today,
        })
    )

    days = forms.MultipleChoiceField()


class EditScheduleForm(forms.Form):
    days = [(i.day, i.day) for i in Schedule.objects.filter(day__gte=date.today())]
    available_hours = (('10:00', '10:00'), ('10:30', '10:30'),
                       ('11:00', '11:00'), ('11:30', '11:30'),
                       ('12:00', '12:00'), ('12:30', '12:30'),
                       ('13:00', '13:00'), ('13:30', '13:30'),
                       ('14:00', '14:00'), ('14:30', '14:30'),
                       ('15:00', '15:00'), ('15:30', '15:30'),
                       ('16:00', '16:00'), ('16:30', '16:30'),
                       ('17:00', '17:00'), ('17:30', '17:30'),
                       ('18:00', '18:00'), ('18:30', '18:30'),
                       ('19:00', '19:00'), ('19:30', '19:30'),
                       ('20:00', '20:00'), ('20:30', '20:30'),
                       ('21:00', '21:00'))
    date = forms.DateField(
        widget=forms.Select(
            attrs={'class': 'form-control', 'id': 'date'},
            choices=[('-', 'Выберите дату')] + days,
        ),
        label='Дата')

    hours = forms.MultipleChoiceField(widget=forms.SelectMultiple(
        attrs={'class': 'form-control', 'size': 5}),
        choices=available_hours,
        label='Часы',
        )
