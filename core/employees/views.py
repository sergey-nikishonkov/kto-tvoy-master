import json
from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.generic.edit import FormView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Employees, Schedule, Hours
from .forms import EmployeeLogingForm, AddScheduleForm, EditScheduleForm
from .schedule_tools import edit_work_hours, add_work_days


class EmployeeLogInView(LoginView):
    """LogIN for employees"""
    template_name = 'employees/master_profile/loging.html'
    form_class = EmployeeLogingForm

    def get_success_url(self):
        return reverse_lazy('schedule')


class EmployeeLogOutView(LogoutView):
    """LogOut for employees"""
    next_page = reverse_lazy('home')


class AddSchedule(LoginRequiredMixin, FormView):
    """This class provides range of dates and saves date in database"""

    form_class = AddScheduleForm
    template_name = 'employees/master_profile/add_schedule.html'
    raise_exception = True
    success_url = reverse_lazy('schedule')
    _choices = []

    def get(self, request, *args, **kwargs):
        """Return days from date-range"""
        if request.GET:
            start = date.fromisoformat(request.GET['start'])
            end = date.fromisoformat(request.GET['end'])
            schedule = [i.day for i in Schedule.objects.filter(day__gte=date.today())]
            if start == end and start not in schedule:
                res = {1: f"{start.strftime('%d.%m')}"}
                return JsonResponse(data=json.dumps(res), safe=False)
            diff = end - start
            res = []
            for i in range(diff.days + 1):
                day = (start + timedelta(days=i))
                if day not in schedule:
                    day = day.strftime('%d.%m')
                    res.append(day)
                    self._choices.append((day, day))
            return JsonResponse(data=json.dumps(res), safe=False)
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """Add days to master`s schedule"""
        form = self.get_form()
        form.fields['days'].choices = self._choices
        if form.is_valid():
            add_work_days(form.cleaned_data['days'], request.user.employees)
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master'] = Employees.objects.get(user=self.request.user)
        return context


class EditSchedule(LoginRequiredMixin, FormView):
    """Allows to add and delete work hours"""
    form_class = EditScheduleForm
    model = Schedule
    template_name = 'employees/master_profile/edit_schedule.html'
    success_url = reverse_lazy('edit_schedule')
    raise_exception = True

    def get(self, request, *args, **kwargs):
        if request.GET:
            try:
                checked_hours = Hours.objects.filter(schedule__day=request.GET['date'])
                hours = [(i.hour.strftime('%H:%M'), i.booked) for i in checked_hours]
                return JsonResponse(data=json.dumps(hours), safe=False)
            except ValidationError:
                return self.render_to_response(self.get_context_data())
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """Add or delete work hours"""
        form = self.get_form()
        if form.is_valid():
            edit_work_hours(form.cleaned_data['date'], form.cleaned_data['hours'])
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master'] = Employees.objects.get(user=self.request.user)
        return context


class ScheduleList(LoginRequiredMixin, ListView):
    pass


class DeleteDay(DeleteView):
    model = Schedule
    success_url = reverse_lazy('edit_schedule')
