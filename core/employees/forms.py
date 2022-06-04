from datetime import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class EmployeeLogingForm(AuthenticationForm):
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


class DateRangeForm(forms.Form):
    today = datetime.now().strftime('%Y-%m-%d')
    start = forms.CharField(
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
