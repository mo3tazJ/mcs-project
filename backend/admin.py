from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from .models import *


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "address")


class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ("department", "role",)
    list_display = ("__str__", "username", "department",
                    "role", "mobile", "email", "is_staff")
    fields = ["username", "password", "mobile", "first_name", "last_name", "email", "department",
              "role", "about", "is_superuser", "is_staff", "is_active", "date_joined", "last_login", "groups", "user_permissions", 'fcm_token']
    readonly_fields = ["date_joined", "last_login"]


class DeviceAdmin(admin.ModelAdmin):
    list_filter = ("device_type", "employee", "is_active", "brand")
    list_display = ("name", "employee", "device_type", "brand", "model",
                    "os", "is_active")


class AccessoryAdmin(admin.ModelAdmin):
    list_filter = ("accessory_type", "device", "brand")
    list_display = ("name", "device", "accessory_type", "brand", "model")


class ServiceAdmin(admin.ModelAdmin):
    list_filter = ("servie_type", "servie_location", "priority_level", "state")
    list_display = ("name", "employee", "worker", "device", "state",
                    "servie_type", "servie_location", "priority_level")
    # fields = ["name", "description", "employee", "servie_type", "subtype", "device",
    #           "servie_location", "priority_level", "worker", "diagnose", "solution",
    #           "notes", "state", "state_changed", "pending_at", "rejected_at", "approved_at", "started_at", "ended_at", "closed_at", "archived_at", "estimated_time", "created_at", "updatet_at"]
    readonly_fields = ["created_at", "updatet_at"]


# Django 4.2
@admin.display(description="Employee")
def emp(obj):
    return f"{obj.service.employee}"


@admin.display(description="Worker")
def workr(obj):
    return f"{obj.service.worker}"


class FeedbackAdmin(admin.ModelAdmin):
    list_filter = ("rate", "service__employee", "service__worker")
    # Django 5.1 With __ operator
    # list_display = ("name", "service", "service__employee",
    #                 "rate", "service__worker")
    # Django 4.2
    list_display = ("name", "service", emp, workr,
                    "rate",)


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Role)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(DeviceType)
admin.site.register(AccessoryType)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(ServiceType)
admin.site.register(ServiceLocation)
admin.site.register(Subtype)
admin.site.register(PriorityLevel)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Feedback, FeedbackAdmin)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # date_hierarchy = 'action_time'
    readonly_fields = ['user', 'content_type', 'object_id',
                       'object_repr', 'action_flag', 'action_time', 'change_message']
    list_filter = ['user', 'action_flag']
    search_fields = ['object_repr', 'change_message']
    list_display = ['__str__', 'user', 'action_flag',
                    'action_time', 'content_type', 'object_id']
