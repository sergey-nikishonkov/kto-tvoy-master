from django.urls import path
from .views import AddSchedule, EmployeeLogInView, EmployeeLogOutView, EditSchedule, ScheduleList

urlpatterns = [
    path('login/', EmployeeLogInView.as_view(), name='master_login'),
    path('logout/', EmployeeLogOutView.as_view(), name='logout'),
    path('schedule/', AddSchedule.as_view(), name='schedule'),
    path('schedule/edit/', EditSchedule.as_view(), name='edit_schedule'),
    path('schedule/list/', ScheduleList.as_view(), name='date_list'),
    path('schedule/delete/<int:pk>', EditSchedule.as_view(), name='delete_day'),
]
