from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from django.contrib.auth.models import User  # AbstractUser, Group, Permission
from django.urls import reverse


class Department(models.Model):

    name = models.CharField("Department Name", max_length=100, unique=True)
    phone = models.CharField("Phone", max_length=100)
    address = models.CharField("Address", max_length=100)
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Department")
        verbose_name_plural = ("Departments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Department_detail", kwargs={"pk": self.pk})


class Role(models.Model):

    name = models.CharField("User Role", max_length=100, unique=True)
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Role")
        verbose_name_plural = ("Roles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Role_detail", kwargs={"pk": self.pk})


class Employee(User):

    # Employee Fields
    mobile = models.CharField("Mobile No.", max_length=25, unique=True, help_text=(
        "Mobile Number Format Example: 0999123456"))
    department = models.ForeignKey(Department, verbose_name=(
        "Department"), on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    role = models.ForeignKey(Role, verbose_name=(
        "Role"), on_delete=models.SET_NULL, related_name="employees", null=True, blank=True)
    about = models.TextField(blank=True)  # , null=True
    fcm_token = models.CharField(
        "FCM Token", max_length=255, null=True, blank=True)
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    def fullname(self):
        return (self.first_name + self.last_name)

    class Meta:
        verbose_name = ("Employee")
        verbose_name_plural = ("Employees")

    def save(self, *args, **kwargs):
        if len(self.password) < 50:
            self.set_password(raw_password=self.password)
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse("Employee_detail", kwargs={"pk": self.pk})


class DeviceType(models.Model):

    name = models.CharField("Device Type", max_length=100, unique=True)
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Device Type")
        verbose_name_plural = ("Device Types")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("DeviceType_detail", kwargs={"pk": self.pk})


class AccessoryType(models.Model):

    name = models.CharField("Accessory Type", max_length=100, unique=True)
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Accessory Type")
        verbose_name_plural = ("Accessory Types")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("AccessoryType_detail", kwargs={"pk": self.pk})


class Device(models.Model):

    name = models.CharField("Device", max_length=100)
    brand = models.CharField("Brand", max_length=100)
    model = models.CharField("Model", max_length=100, blank=True)
    device_type = models.ForeignKey(DeviceType, verbose_name=(
        "Device Type"), on_delete=models.SET_NULL, related_name="devices", null=True, blank=True)
    employee = models.ForeignKey(Employee, verbose_name=(
        "Employee"), on_delete=models.SET_NULL, related_name="devices", null=True, blank=True)
    sn = models.CharField("Serial Number", max_length=100, blank=True)
    os = models.CharField("Operating System", max_length=100, blank=True)
    specs = models.TextField("Technical Specifications", blank=True)
    anydesk = models.CharField(
        "AnyDesk Address", max_length=100, blank=True)
    notes = models.TextField("Notes", blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Device")
        verbose_name_plural = ("Devices")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Device_detail", kwargs={"pk": self.pk})


class Accessory(models.Model):

    name = models.CharField("Accessory", max_length=100)
    brand = models.CharField("Brand", max_length=100)
    model = models.CharField("Model", max_length=100, blank=True)
    accessory_type = models.ForeignKey(AccessoryType, verbose_name=(
        "Accessory Type"), on_delete=models.SET_NULL, related_name="accessories", null=True, blank=True)
    device = models.ForeignKey(Device, verbose_name=(
        "Linked Device"), on_delete=models.SET_NULL, related_name="accessories", null=True, blank=True)
    sn = models.CharField("Serial Number", max_length=100, blank=True)
    notes = models.TextField("Notes", blank=True)

    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Accessory")
        verbose_name_plural = ("Accessories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Accessory_detail", kwargs={"pk": self.pk})


class ServiceType(models.Model):

    name = models.CharField("Service Type", max_length=100, unique=True)
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Service Type")
        verbose_name_plural = ("Service Types")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ServiceType_detail", kwargs={"pk": self.pk})


class Subtype(models.Model):  # Rename it to Subtype

    name = models.CharField("Subtype", max_length=100, unique=True)
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Subtype")
        verbose_name_plural = ("Subtypes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Subtype_detail", kwargs={"pk": self.pk})


class ServiceLocation(models.Model):

    name = models.CharField("Service Location", max_length=100, unique=True)
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Service Location")
        verbose_name_plural = ("Service Locations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ServiceLocation_detail", kwargs={"pk": self.pk})


class PriorityLevel(models.Model):

    name = models.CharField("Priority Level", max_length=100, unique=True)
    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Priority Level")
        verbose_name_plural = ("Priority Levels")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("PriorityLevel_detail", kwargs={"pk": self.pk})


class Service(models.Model):

    name = models.CharField("Service Name", max_length=100)
    description = models.TextField("Description")

    employee = models.ForeignKey(Employee, verbose_name=(
        "Employee"), on_delete=models.SET_NULL, related_name="empservices", null=True)
    device = models.ForeignKey(Device, verbose_name=(
        "Device"), on_delete=models.SET_NULL, related_name="services", null=True, blank=True)
    servie_type = models.ForeignKey(ServiceType, verbose_name=(
        "Service Type"), on_delete=models.SET_NULL, related_name="services", null=True)
    subtype = models.ForeignKey(Subtype, verbose_name=(
        "Subtype"), on_delete=models.SET_NULL, related_name="services", blank=True, null=True)
    servie_location = models.ForeignKey(ServiceLocation, verbose_name=(
        "Service Location"), on_delete=models.SET_NULL, related_name="services", null=True)
    priority_level = models.ForeignKey(PriorityLevel, verbose_name=(
        "Priority Level"), on_delete=models.SET_NULL, related_name="services", null=True)
    worker = models.ForeignKey(Employee, verbose_name=(
        "Worker"), on_delete=models.SET_NULL, related_name="wrkservices", null=True, blank=True)

    diagnose = models.TextField("Diagnose", blank=True)
    solution = models.TextField("Solution", blank=True)
    notes = models.TextField("Notes", blank=True)
    reason = models.TextField("Reason", blank=True)

    STATUS = Choices('pending', 'rejected', 'approved',
                     'started', 'ended', 'closed', 'archived')
    state = StatusField()
    state_changed = MonitorField(monitor='state')
    pending_at = MonitorField(monitor='state', when=['pending'])
    rejected_at = MonitorField(monitor='state', when=[
                               'rejected'], default=None, blank=True, null=True)
    approved_at = MonitorField(monitor='state', when=[
                               'approved'], default=None, blank=True, null=True)
    started_at = MonitorField(monitor='state', when=[
                              'started'], default=None, blank=True, null=True)
    ended_at = MonitorField(monitor='state', when=[
                            'ended'], default=None, blank=True, null=True)
    closed_at = MonitorField(monitor='state', when=[
                             'closed'], default=None, blank=True, null=True)
    archived_at = MonitorField(monitor='state', when=[
                               'archived'], default=None, blank=True, null=True)
    estimated_time = models.DecimalField(
        "Estimated Time", max_digits=10, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField("Created", auto_now_add=True)
    updatet_at = models.DateTimeField("Updated", auto_now=True)

    class Meta:
        verbose_name = ("Service")
        verbose_name_plural = ("Services")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Service_detail", kwargs={"pk": self.pk})


class Feedback(models.Model):

    name = models.CharField("Feedback Name", max_length=100)
    service = models.OneToOneField(Service, verbose_name=(
        "Service"), on_delete=models.CASCADE)
    rate = models.IntegerField(
        "Rate", validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)  # , null=True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Feedback")
        verbose_name_plural = ("Feedbacks")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Feedback_detail", kwargs={"pk": self.pk})
        # return reverse("feedback-report")
