import json
from datetime import datetime, date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from .models import Employees, Schedule
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import EmployeeLogingForm, DateRangeForm


class EmployeeLogInView(LoginView):
    template_name = 'employees/master_profile/loging.html'
    form_class = EmployeeLogingForm

    def get_success_url(self):
        return reverse_lazy('schedule')


class EmployeeLogOutView(LogoutView):
    next_page = reverse_lazy('home')


class AddSchedule(LoginRequiredMixin, FormView):
    form_class = DateRangeForm
    template_name = 'employees/master_profile/add_schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master'] = Employees.objects.get(user=self.request.user)
        return context


def ajax_add_schedule(request):
    master = Employees.objects.get(user=request.user)
    year = datetime.now().year
    for value in request.GET.values():
        day_month = value.split('.')
        schedule = Schedule(master=master, day=date(year, int(day_month[1]),  int(day_month[0])))
        schedule.save()
    return redirect('/')


def ajax_days_schedule(request):
    if 'start' in request.GET:
        get_start = request.GET['start']
        get_end = request.GET['end']
        if get_start == get_end:
            res = {1: f"{get_end.split('-')[2]}.{get_start.split('-')[1]}"}
            return JsonResponse(data=json.dumps(res), safe=False)
        start = datetime(*[int(i) for i in get_start.split('-')])
        end = datetime(*[int(i) for i in get_end.split('-')])
        diff = end - start
        schedule = [i.day for i in Schedule.objects.filter(day__gte=date.today())]
        res = []
        for i in range(diff.days+1):
            day = (start + timedelta(days=i)).date()
            if day not in schedule:
                res.append(day.strftime('%d.%m'))
        return JsonResponse(data=json.dumps(res), safe=False)
    else:
        return JsonResponse(data=json.dumps([]), safe=False)
