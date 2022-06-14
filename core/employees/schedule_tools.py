"""
This module provides tools which is using for add and delete Hours form database;
and also add days to Schedule
"""

from typing import List
from datetime import date
from employees.models import Employees, Schedule, Hours


def edit_work_hours(day: date, hours: List[str]) -> None:
    """Add or delete work hours from database"""
    available_hours = ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30',
                       '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
                       '16:00', '16:30', '17:00', '17:30', '18:00', '18:30',
                       '19:00', '19:30', '20:00', '20:30', '21:00', ]
    schedule = Schedule.objects.get(day=day)
    res = set(available_hours) - set(hours)
    Hours.objects.filter(schedule__day=day, hour__in=res).delete()
    for hour in hours:
        Hours.objects.get_or_create(schedule=schedule, hour=hour)


def add_work_days(days: List[str], employee: Employees) -> None:
    """Save work days in database"""
    year = date.today().year
    for day in days:
        day_month = day.split('.')
        day = date(year, int(day_month[1]), int(day_month[0]))
        Schedule.objects.create(master=employee, day=day)
