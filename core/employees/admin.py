from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Employees, Schedule, Hours


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display_links = ('get_first_name', 'get_last_name',)
    list_display = ('get_first_name', 'get_last_name', 'position', 'get_photo',)

    @admin.display(description='Имя')
    def get_first_name(self, obj):
        """Get first name from User object"""
        return obj.user.first_name

    @admin.display(description='Фамилия')
    def get_last_name(self, obj):
        """Get last name from User object"""
        return obj.user.last_name

    @admin.display(description='Фото')
    def get_photo(self, obj):
        """Show master`s photo at admin panel"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        return 'No photo'


class InlineHours(admin.StackedInline):
    model = Hours
    fields = ['hour', 'booked']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['master', 'day', 'is_reserved_hours']
    inlines = [InlineHours]


@admin.register(Hours)
class HoursAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'hour', 'booked']
