from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


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

    class Meta(object):
        model = Employee
        exclude = ['created_at', 'updatet_at', 'password']
        # fields = "__all__"
        # fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name',
        #           'is_superuser', 'is_staff', 'department', 'role', 'mobile', 'about']


class SvcEmployeeSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Employee
        # fields = "__all__"
        fields = ['fullname', 'username', 'first_name', 'last_name']


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = DeviceType
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class AccessoryTypeSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = AccessoryType
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class DeviceSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Device
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class SvcDeviceSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Device
        fields = ("name",)


class AccessorySerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Accessory
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ServiceType
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class SvcServiceTypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ServiceType
        fields = ("name",)


class ServiceLocationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ServiceLocation
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class SvcServiceLocationSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ServiceLocation
        fields = ("name",)


class SubtypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Subtype
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class SvcSubtypeSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Subtype
        fields = ("name",)


class PriorityLevelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PriorityLevel
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class SvcPriorityLevelSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = PriorityLevel
        fields = ("name",)


class ServiceSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Service
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']


class SvcServiceSerializer(serializers.ModelSerializer):

    # subtype = SubtypeSerializer()
    class Meta(object):
        model = Service
        fields = "__all__"

    # def create(self, validated_data):
    #     validated_data['user'] = self.context["request"].user
    #     return super(SvcServiceSerializer, self).create(validated_data)


class FeedbackSerializer(serializers.ModelSerializer):

    # service = ServiceSerializer()

    class Meta(object):
        model = Feedback
        # fields = "__all__"
        exclude = ['created_at', 'updatet_at']
