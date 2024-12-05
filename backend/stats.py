from django.db import connection
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .models import *
from .serializers import *
from .reports import *
from .stats import *
from django.db.models import Count, Avg, Min, Max, StdDev, Variance


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_stats(request):
    # Services Stats
    all_sevices = Service.objects.only(
        "servie_type", "priority_level", "state", "subtype", "servie_location")
    stats = {}

    stats["Services Count"] = all_sevices.count()
    stats["Average Rating"] = all_sevices.aggregate(Avg("feedback__rate"))[
        "feedback__rate__avg"]
    # Priority Levels
    priority = {}
    for p in PriorityLevel.objects.only("name"):
        priority[p.name] = all_sevices.filter(
            priority_level__name=p.name).count()

    # State
    states = {}
    for st in ['pending', 'rejected', 'approved', 'started', 'ended', 'closed', 'archived']:
        states[st] = all_sevices.filter(state=st).count()

    # Service Type
    types = {}
    for t in ServiceType.objects.only("name"):
        types[t.name] = all_sevices.filter(
            servie_type__name=t.name).count()

    # subtypes
    subtypes = {}
    for s in Subtype.objects.only("name"):
        subtypes[s.name] = all_sevices.filter(
            subtype__name=s.name).count()
    # # sub = []
    # # for svc in all_sevices:
    # #     # print(type(svc.subtype.name))
    # #     # print(svc.subtype.name)
    # #     sub.append(svc.subtype.name)
    # # for st in sub:
    # #     subtypes[st] = all_sevices.filter(
    # #         subtype__name=st).count()

    # locations
    locations = {}
    for l in ServiceLocation.objects.only("name"):
        locations[l.name] = all_sevices.filter(
            servie_location__name=l.name).count()

    services = {"stats": stats, "states": states,
                "priority": priority, "types": types, "subtypes": subtypes, "locations": locations}

    # Feedback Stats
    all_feedbacks = Feedback.objects.only("rate")
    feedbacks = {}
    feedbacks_stats = all_feedbacks.aggregate(Count("rate"), Avg("rate"), Max(
        "rate"), Min("rate"), StdDev("rate"), Variance("rate"))

    feedbacks["Count"] = feedbacks_stats[
        "rate__count"]
    feedbacks["Average"] = feedbacks_stats[
        "rate__avg"]
    feedbacks["Minimum"] = feedbacks_stats[
        "rate__min"]
    feedbacks["Maximum"] = feedbacks_stats[
        "rate__max"]
    feedbacks["STD Deviation"] = feedbacks_stats[
        "rate__stddev"]
    feedbacks["Variance"] = feedbacks_stats[
        "rate__variance"]

    # Devices Stats
    all_devices = Device.objects.only(
        "is_active", "device_type", "employee", "brand")
    device_stats = {}
    device_stats["Devices Count"] = all_devices.count()
    device_stats["Active Devices"] = all_devices.filter(
        is_active=True).count()
    device_stats["In Use"] = all_devices.filter(
        employee__isnull=False).count()

    # Device Types
    device_types = {}

    for dt in DeviceType.objects.only("name"):
        device_types[dt.name] = all_devices.filter(
            device_type__name=dt.name).count()

    # Device Brands
    device_brands = {}
    for b in all_devices.only("brand"):
        device_brands[b.brand] = all_devices.filter(
            brand=b.brand).count()

    devices = {"Stats": device_stats,
               "Types": device_types, "Brands": device_brands}

    # Accessories Stats
    all_accessories = Accessory.objects.only("accessory_type")
    accessories_stats = {}
    accessories_stats["Accessories Count"] = all_accessories.count()
    accessory_types = {}
    for a in AccessoryType.objects.only("name"):
        accessory_types[a.name] = all_accessories.filter(
            accessory_type__name=a.name).count()

    accessories = {"Stats": accessories_stats,
                   "Types": accessory_types}

    # Employees Stats
    all_employees = Employee.objects.only(
        "is_active", "is_staff", "role", "department")
    employees_stats = {}
    employees_stats["Employees Count"] = all_employees.count()
    employees_stats["Active Users"] = all_employees.filter(
        is_active=True).count()
    employees_stats["Admins Count"] = all_employees.filter(
        is_staff=True).count()
    employees_stats["Techs Count"] = all_employees.filter(
        role__name="Tech").count()
    employees_stats["Clients Count"] = all_employees.filter(
        role__name="Client").count()

    # Employees Departments
    departments = {}
    for d in Department.objects.only("name"):
        departments[d.name] = all_employees.filter(
            department__name=d.name).count()

    employees = {"Stats": employees_stats,
                 "departments Employees Count": departments}

    # print(len(connection.queries))
    return Response({"services": services, "feedbacks": feedbacks,  "devices": devices, "accessories": accessories, "employees": employees})
