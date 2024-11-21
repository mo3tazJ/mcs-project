from django.urls import path, re_path
from . import views

urlpatterns = [
    # path("welcome", views.welcome),
    # path("about", views.about),
    path("", views.index, name="index"),
    path("login", views.log_in, name="login"),
    re_path("logout", views.log_out),
    path("test_token", views.test_token),
    path("department", views.get_departments),
    path("department/<int:id>", views.get_department_by_id),
    path("role", views.get_roles),
    path("role/<int:id>", views.get_role_by_id),
    path("employee", views.get_employees),
    path("employee/<int:id>", views.get_employee_by_id),
    path("service", views.get_services),
    path("service/<int:id>", views.get_service_by_id),

]
