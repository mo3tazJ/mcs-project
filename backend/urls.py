from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views, reports, stats

router = DefaultRouter()
router.register("api/department", viewset=views.DepartmentViewSet)
router.register("api/role", viewset=views.RoleViewSet)
router.register("api/employee", viewset=views.EmployeeViewSet)
router.register("api/device-type", viewset=views.DeviceTypeViewSet)
router.register("api/accessory-type", viewset=views.AccessoryTypeViewSet)
router.register("api/device", viewset=views.DeviceViewSet)
router.register("api/accessory", viewset=views.AccessoryViewSet)
router.register("api/service-type", viewset=views.ServiceTypeViewSet)
router.register("api/subtype", viewset=views.SubtypeViewSet)
router.register("api/service-location", viewset=views.ServiceLocationViewSet)
router.register("api/priority-level", viewset=views.PriorityLevelViewSet)
router.register("api/service", viewset=views.ServiceViewSet)
router.register("api/feedback", viewset=views.FeedbackViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("admin-page", views.adminPage, name="admin-page"),
    path("login", views.log_in, name="login"),
    re_path("logout", views.log_out),
    path("get-employee-devices", views.get_employee_devices),
    path("get-employee-services", views.get_employee_services),
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
    path("", include(router.urls)),

]
