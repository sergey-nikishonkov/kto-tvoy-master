from django.urls import path
from .views import AddSchedule, EmployeeLogInView, EmployeeLogOutView

urlpatterns = [
    path('login/', EmployeeLogInView.as_view(), name='master_login'),
    path('logout/', EmployeeLogOutView.as_view(), name='logout'),
    path('schedule/', AddSchedule.as_view(), name='schedule'),
]
