import json
from datetime import date, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .models import Employees, Schedule
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
    choices = []

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
                    self.choices.append((day, day))
            return JsonResponse(data=json.dumps(res), safe=False)
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        Add days to master`s schedule
        """
        form = self.get_form()
        form.fields['days'].choices = self.choices
        if form.is_valid():
            master = Employees.objects.get(user=request.user)
            values = form.cleaned_data['days']
            year = date.today().year
            for value in values:
                day_month = value.split('.')
                day = date(year, int(day_month[1]), int(day_month[0]))
                schedule = Schedule(master=master, day=day)
                schedule.save()
            return(redirect('/'))
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master'] = Employees.objects.get(user=self.request.user)
        return context


class EditSchedule(LoginRequiredMixin, FormView):
    form_class = EditScheduleForm
    model = Schedule
    context_object_name = 'schedule'
    template_name = 'employees/master_profile/edit_schedule.html'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        if request.GET:
            chosen_date = Schedule.objects.get(day=request.GET['date'])
            checked_hours = Hours.objects.filter(schedule=chosen_date)
            hours = [(i.hour.strftime('%H:%M'), i.booked) for i in checked_hours]
            return JsonResponse(data=json.dumps(hours), safe=False)
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master'] = Employees.objects.get(user=self.request.user)
        return context

