from datetime import datetime
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
    today = datetime.now().strftime('%Y-%m-%d')
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


class AddScheduleForm(forms.ModelForm):
    """Add work-days in Schedule model"""
    class Meta:
        model = Schedule
        fields = ('master', 'day')
