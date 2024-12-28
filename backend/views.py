from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import *
from .serializers import *
from .reports import *
from .stats import *
from django.db.models import Sum, Count, Avg
from backend.fcm.messaging import sendFcm


def index(request):
    return render(request, "backend/home.html")


def about(request):
    return render(request, "backend/about.html")


def adminPage(request):
    return render(request, "backend/admin-page.html")


# notification test
@api_view(['POST'])
def send_notification(request):
    sendFcm(fcm="cByANuUuSgSU71W6ptMWOD:APA91bHelhpay1mLD88266asNK44T3Hd4VAS3BBzDeH1aOqNyyNX0iSaKtjyHQOJc58nlT4TsDm5Sm4ZWVS3kEVfbYK0NOoYGXp4shv1LLwRbrin4qA4CGk", title="title", body="body")
    return Response({"token": "token.key", "user": "emp_serializer.data"})


##########################
# Login And Authintication
##########################
@api_view(['POST'])
def log_in(request):
    employee = get_object_or_404(Employee, username=request.data['username'])

    if not employee.check_password(request.data['password']):
        return Response({"detail": "Not Found"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=employee)
    session_hash = employee.get_session_auth_hash()

    emp_serializer = EmployeeSerializer(instance=employee)
    employee.fcm_token = request.data['fcm_token']
    employee.save()
    return Response({"token": token.key, "user": emp_serializer.data})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def log_out(request):
    employee = get_object_or_404(Employee, username=request.data['username'])
    # token = Token.objects.get(user=employee)
    # token.delete()
    # session_hash = employee.get_session_auth_hash()

    if employee.fcm_token:
        employee.fcm_token = ""
        employee.save()
    if request.user.auth_token:
        request.user.auth_token.delete()
        return Response({"Details": "Logged Out!"}, status=status.HTTP_200_OK)
    else:
        return Response({"Details": "Not Logged In!"}, status=status.HTTP_400_BAD_REQUEST)


##############
# Models APIs

# Department:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_departments(request):
    departments = Department.objects.all()
    deptserializer = DepartmentSerializer(departments, many=True)
    return Response({"departments": deptserializer.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_department_by_id(request, id):
    department = get_object_or_404(Department, pk=id)
    serialized = DepartmentSerializer(department)
    return Response({"department": serialized.data, "name": serialized.data['name']})


# Role:
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_roles(request):
    roles = Role.objects.all()
    serialized = RoleSerializer(roles, many=True)
    return Response({"roles": serialized.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_role_by_id(request, id):
    role = get_object_or_404(Role, pk=id)
    serialized = RoleSerializer(role)
    return Response({"role": serialized.data})


# Employee:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_employees(request):
    employees = Employee.objects.all()
    serialized = EmployeeSerializer(employees, many=True)
    return Response({"employees": serialized.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])  # , IsAdminUser
def get_employee_by_id(request, id):
    employee = get_object_or_404(Employee, pk=id)
    deptserialized = DepartmentSerializer(employee.department)
    roleserialized = RoleSerializer(employee.role)
    empdevices = Device.objects.filter(employee=id)
    deviceserialized = DeviceSerializer(empdevices, many=True)
    serialized = EmployeeSerializer(employee)
    return Response({"employee": serialized.data, "department": deptserialized.data, "role": roleserialized.data, "devices": deviceserialized.data})


# Service:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_services(request):
    services = Service.objects.all()
    serialized = ServiceSerializer(services, many=True)
    return Response({"services": serialized.data, "echo": request.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_service_by_id(request, id):
    service = get_object_or_404(Service, pk=id)
    serialized = ServiceSerializer(service)
    return Response({"service": serialized.data})


# ViewSets
# Department Viewset
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Role Viewset
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Employee Viewset
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Device Type Viewset
class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Accessory Type Viewset
class AccessoryTypeViewSet(viewsets.ModelViewSet):
    queryset = AccessoryType.objects.all()
    serializer_class = AccessoryTypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Device Viewset
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Accessory Viewset
class AccessoryViewSet(viewsets.ModelViewSet):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Service Type Viewset
class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Subtype Viewset
class SubtypeViewSet(viewsets.ModelViewSet):
    queryset = Subtype.objects.all()
    serializer_class = SubtypeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# ServiceLocation Viewset
class ServiceLocationViewSet(viewsets.ModelViewSet):
    queryset = ServiceLocation.objects.all()
    serializer_class = ServiceLocationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# PriorityLevel Viewset
class PriorityLevelViewSet(viewsets.ModelViewSet):
    queryset = PriorityLevel.objects.all()
    serializer_class = PriorityLevelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Service Viewset
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Feedback Viewset
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


###################


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_employee_devices(request):
    # emp = get_object_or_404(Employee, username=request.data['username'])
    emp = get_object_or_404(Employee, pk=request.data['id'])
    deptserializer = DepartmentSerializer(emp.department)
    empdevices = Device.objects.filter(employee=emp)
    devserializer = DeviceSerializer(empdevices, many=True)
    return Response({"devices": devserializer.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_employee_services(request):
    emp = get_object_or_404(Employee, pk=request.data['id'])
    empservices = Service.objects.filter(employee=emp)
    srvserializer = ServiceSerializer(empservices, many=True)
    return Response({"services": srvserializer.data})


# Add Service
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_service(request, *args, **kwargs):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # print(serializer.validated_data)
        instance = serializer.save()
        # print(serializer.data)
        return Response({"message": "Service Added"})
    return Response({"message": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)


# Add Service1
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_service1(request):
    service = Service()

    employee = get_object_or_404(
        Employee, pk=request.data['client_id'])
    servie_type = get_object_or_404(
        ServiceType, pk=request.data['service_type_id'])
    subtype = get_object_or_404(
        Subtype, pk=request.data['subtype_id'])
    servie_location = get_object_or_404(
        ServiceLocation, pk=request.data['service_location_id'])
    if request.data['device_id'] != 0:
        device = get_object_or_404(
            Device, pk=request.data['device_id'])
        service.device = device
    priority_level = get_object_or_404(
        PriorityLevel, pk=request.data['priority_level_id'])
    print(request.data)

    print(request.data['client_id'])

    service.employee = employee
    service.name = request.data['name']
    service.description = request.data['description']
    service.servie_type = servie_type
    service.subtype = subtype
    service.servie_location = servie_location
    service.priority_level = priority_level

    service.save()

    return Response({"message": "Service Added"}, status=status.HTTP_200_OK)


# Manager Service Process
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def process_service_mgr(request):
    service = get_object_or_404(Service, pk=request.data['id'])
    worker = get_object_or_404(
        Employee, pk=request.data['worker'])

    print(request.data)

    print(service)
    print(service.state)

    service.state = request.data['state']
    if service.state == "approved":
        service.worker = worker
    if service.state == "rejected":
        service.reason = request.data['reason']

    service.save()
    print(service.state)
    serializer = ServiceSerializer(service)
    return Response({"message": "Service Updated", "data": serializer.data}, status=status.HTTP_200_OK)


# Tech Service Process
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def process_service_tech(request):
    service = get_object_or_404(Service, pk=request.data['id'])

    print(request.data)

    print(service)
    print(service.state)

    service.state = request.data['state']
    service.diagnose = request.data['diagnose']
    service.notes = request.data['notes']
    print(service)
    # service.save()
    print(service.state)
    serializer = ServiceSerializer(service)
    return Response({"message": "Service Updated", "data": serializer.data}, status=status.HTTP_200_OK)


# Add Feedback
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_feedback(request, *args, **kwargs):
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        # print(serializer.data)
        return Response({"message": "Feedback Added"})
    return Response({"message": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)
