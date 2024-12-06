from django.urls import path, re_path
from . import views, reports, stats

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
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
    path("stats", stats.get_stats),
    path("reports/service", reports.ServiceReport.as_view()),
    path("reports/service-tech", reports.ServiceByTechReport.as_view()),
    path("reports/feedback", reports.FeedbackReport.as_view()),
    path("reports/device", reports.DeviceReport.as_view()),

]
