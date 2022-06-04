from django.shortcuts import render
from employees.models import Employees


def home(request):
    masters = Employees.objects.filter()
    return render(request, 'online_booking/index.html', {'masters': masters})