from django.urls import path
from .views import AddSchedule, ajax_add_schedule, ajax_days_schedule,EmployeeLogInView, EmployeeLogOutView

urlpatterns = [
    path('login/', EmployeeLogInView.as_view(), name='master_login'),
    path('logout/', EmployeeLogOutView.as_view(), name='logout'),
    path('schedule/', AddSchedule.as_view(), name='schedule'),
    path('ajax/add_days/', ajax_days_schedule, name='add_days'),
    path('ajax/add_schedule/', ajax_add_schedule, name='add_schedule'),
]
