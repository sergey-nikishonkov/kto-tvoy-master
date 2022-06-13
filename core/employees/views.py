import json
from datetime import date, timedelta, time
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.generic.edit import FormView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Employees, Schedule, Hours
from .forms import EmployeeLogingForm, AddScheduleForm, EditScheduleForm


class EmployeeLogInView(LoginView):
    template_name = 'employees/master_profile/loging.html'
    form_class = EmployeeLogingForm

    def get_success_url(self):
        return reverse_lazy('schedule')


class EmployeeLogOutView(LogoutView):
    next_page = reverse_lazy('home')


class AddSchedule(LoginRequiredMixin, FormView):
    """This class provides range of dates and saves date in database"""

    form_class = AddScheduleForm
    template_name = 'employees/master_profile/add_schedule.html'
    raise_exception = True
    success_url = reverse_lazy('schedule')
    _choices = []

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests: instantiate a blank version of the form.
        Return days from date-range
        """
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
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        Add days to master`s schedule
        """
        form = self.get_form()
        form.fields['days'].choices = self._choices
        if form.is_valid():
            values = form.cleaned_data['days']
            year = date.today().year
            for value in values:
                day_month = value.split('.')
                day = date(year, int(day_month[1]), int(day_month[0]))
                Schedule.objects.create(master=request.user.employees, day=day)
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master'] = Employees.objects.get(user=self.request.user)
        return context


class EditSchedule(LoginRequiredMixin, FormView):
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
        form = self.get_form()
        if form.is_valid():
            available_hours = ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00',
                 '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30',
                 '21:00']
            schedule = Schedule.objects.get(day=form.cleaned_data['date'])
            res = set(available_hours) - set(form.cleaned_data['hours'])
            Hours.objects.filter(schedule__day=form.cleaned_data['date'], hour__in=res).delete()
            for hour in form.cleaned_data['hours']:
                Hours.objects.get_or_create(schedule=schedule, hour=hour)
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master'] = Employees.objects.get(user=self.request.user)
        return context

class DeleteDay(DeleteView):
    pass