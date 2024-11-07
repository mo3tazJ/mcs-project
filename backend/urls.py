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

]
