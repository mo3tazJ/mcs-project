from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email',
                  "first_name", "last_name", "is_superuser", "is_staff"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Department
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class RoleSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Role
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    role = RoleSerializer()

    class Meta(object):
        model = Employee
        exclude = ['created_at', 'updatet_at', 'password']
        # fields = "__all__"
        # fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name',
        #           'is_superuser', 'is_staff', 'department', 'role', 'mobile', 'about']


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = DeviceType
        fields = "__all__"


class AccessoryTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = AccessoryType
        fields = "__all__"


class DeviceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Device
        fields = "__all__"


class AccessorySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Accessory
        fields = "__all__"


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ServiceType
        fields = "__all__"


class ServiceLocationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ServiceLocation
        fields = "__all__"


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Complaint
        fields = "__all__"


class PriorityLevelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PriorityLevel
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Service
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Feedback
        fields = "__all__"
