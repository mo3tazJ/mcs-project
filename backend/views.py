from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.sessions.models import Session

from .models import *
from .serializers import *
from .reports import *
from .stats import *
from backend.fcm.messaging import sendFcm
from django.db.models import Q
from urllib.request import urlopen
import io


#################
###  General  ###
#################
with urlopen("https://mcsproject.pythonanywhere.com/static/backend/apk/latest.txt") as f:
    for line in io.TextIOWrapper(f, "utf-8"):
        latest_version = line
latest_version_link = f"https://mcsproject.pythonanywhere.com/static/backend/apk/ITMS{latest_version}.apk"


def index(request):
    return render(request, "backend/home.html", {"latest": latest_version, "link": latest_version_link})


def about(request):
    return render(request, "backend/about.html")


# Admin Page
@login_required
def adminPage(request):
    return render(request, "backend/admin-page.html")


def admin_login(request):
    return redirect("/admin/login/?next=/admin-page")


# Manager Broadcast A Message
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def broadcast(request, *args, **kwargs):
    # Broadcast:
    try:
        title = request.data.get('title')
        body = request.data.get('body')
        subs = Employee.objects.exclude(Q(role__name='Manager') | Q(
            fcm_token__isnull=True) | Q(fcm_token=''))
        for sub in subs:
            fcm = sub.fcm_token
            # print(f"{title} \n{body}")
            sendFcm(fcm=fcm, title=title, body=body)
        # serialized = EmployeeSerializer(subs, many=True)
        return Response({"message": "Broadcasted"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "Invalid", "Exception": e}, status=status.HTTP_400_BAD_REQUEST)


# Check For APP Update:
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_update(request):
    current = request.data.get('current')
    latest = latest_version
    if current < latest:
        print(f"There Is A newer Version: {latest}")
        print(latest_version_link)
        return Response({"Details": f"There Is A newer Version: {latest}", "link": latest_version_link}, status=status.HTTP_200_OK)
    else:
        print("You Have The Latest Version")
        return Response({"Details": "You Have The Latest Version"}, status=status.HTTP_200_OK)


################################
##  Login And Authintication  ##
################################
@api_view(['POST'])
def log_in(request):
    employee = get_object_or_404(
        Employee, username=request.data.get('username'))
    if not employee.check_password(request.data.get('password')):
        return Response({"detail": "Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=employee)
    # session_hash = employee.get_session_auth_hash()

    serializer = EmployeeSerializer(instance=employee)
    employee.fcm_token = request.data.get('fcm_token')
    employee.save()
    return Response({"token": token.key, "user": serializer.data})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def log_out(request):
    employee = get_object_or_404(
        Employee, username=request.data.get('username'))
    # token = Token.objects.get(user=employee)
    # token.delete()
    # session_hash = employee.get_session_auth_hash()
    if request.user.auth_token:
        request.user.auth_token.delete()
        if employee.fcm_token:
            employee.fcm_token = ""
            employee.save()
        return Response({"Details": "Logged Out!"}, status=status.HTTP_200_OK)
    else:
        return Response({"Details": "Not Logged In!"}, status=status.HTTP_400_BAD_REQUEST)


###################
##  Models APIs  ##
###################
# Department:
# Get All Departments:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_departments(request):
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response({"departments": serializer.data})


# Get Department By ID:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_department_by_id(request, id):
    department = get_object_or_404(Department, pk=id)
    serializer = DepartmentSerializer(department)
    return Response({"department": serializer.data})


# Role:
# Get All Roles:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_roles(request):
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response({"roles": serializer.data})


# Get Role By ID:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_role_by_id(request, id):
    role = get_object_or_404(Role, pk=id)
    serializer = RoleSerializer(role)
    return Response({"role": serializer.data})


# Employees:
# Get All Employees:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_employees(request):
    employees = Employee.objects.all()
    serialized = EmployeeSerializer(employees, many=True)
    return Response({"employees": serialized.data})


# Get Employee By ID:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_employee_by_id(request, id):
    employee = get_object_or_404(Employee, pk=id)
    serializer = EmployeeSerializer(employee)
    return Response({"employee": serializer.data})


# Get Tech Employees:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_tech_employees(request):
    employees = Employee.objects.filter(role__name='Tech')
    serialized = EmployeeSerializer(employees, many=True)
    return Response({"employees": serialized.data})


# Service:
# Get All Services:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_services(request):
    services = Service.objects.all()
    # serializer = ServiceSerializer(services, many=True)
    serializer = FullServiceSerializer(services, many=True)
    return Response({"services": serializer.data})


# Get Service By ID:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_service_by_id(request, id):
    service = get_object_or_404(Service, pk=id)
    # serializer = ServiceSerializer(service)
    serializer = FullServiceSerializer(service)
    return Response({"service": serializer.data})


# Get Active Services:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_active_services(request):
    # services = Service.objects.all().exclude(state='archived')
    services = Service.objects.filter(~Q(state='archived'))
    # serializer = ServiceSerializer(services, many=True)
    serializer = FullServiceSerializer(services, many=True)
    return Response({"services": serializer.data})


# Get Pending Services (Manager/SysAdmin):
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_pending_services(request):
    services = Service.objects.filter(state='pending')
    # serializer = ServiceSerializer(services, many=True)
    serializer = FullServiceSerializer(services, many=True)
    return Response({"services": serializer.data})


# Get Employee Devices:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_employee_devices(request, id):
    # emp = get_object_or_404(Employee, pk=request.data.get('id'))
    emp = get_object_or_404(Employee, pk=id)
    empdevices = Device.objects.filter(employee=emp)
    devserializer = DeviceSerializer(empdevices, many=True)
    return Response({"devices": devserializer.data})


# Get Employee Services:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_employee_services(request, id):
    # emp = get_object_or_404(Employee, pk=request.data.get('id'))
    emp = get_object_or_404(Employee, pk=id)
    empservices = Service.objects.filter(
        employee=emp).filter(~Q(state='archived'))
    # srvserializer = ServiceSerializer(empservices, many=True)
    srvserializer = FullServiceSerializer(empservices, many=True)
    return Response({"services": srvserializer.data})


# Add Service
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_service(request, *args, **kwargs):
    client = get_object_or_404(Employee, pk=request.data.get('employee'))
    manager = get_object_or_404(Employee, role__name='Manager')
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        # Notification:
        fcm = manager.fcm_token
        title = "New Service Request"
        body = f"Client '{client.get_full_name()}' Added A New Service Request '{serializer.data.get('name')}'"
        # print(title)
        # print(body)
        # print(fcm)
        sendFcm(fcm=fcm, title=title, body=body)
        return Response({"message": "Service Added", "data": serializer.data})
    return Response({"message": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)


# Edit Pending Service By Client
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def edit_service_client(request, *args, **kwargs):
    service = get_object_or_404(Service, pk=request.data.get('id'))
    serializer = ServiceSerializer(data=request.data)
    if service.state == 'pending':
        if serializer.is_valid(raise_exception=True):
            vd = serializer.validated_data
            serializer.update(instance=service, validated_data=vd)
            serialized = FullServiceSerializer(service)
            return Response({"message": "Service Updated", "data": serialized.data})
    if service.state == 'rejected':
        if serializer.is_valid(raise_exception=True):
            vd = serializer.validated_data
            serializer.update(instance=service, validated_data=vd)
            # RePend The Rejected Service:
            service.state = 'pending'
            service.save()
            serialized = FullServiceSerializer(service)
            # Notification
            manager = get_object_or_404(Employee, role__name='Manager')
            fcm = manager.fcm_token
            title = "Re-Pending Rejected Service"
            body = f"Client '{service.employee}' Has Edited his previously Rejected Service '{service.name}', Check it"
            # print(title)
            # print(body)
            # print(fcm)
            sendFcm(fcm=fcm, title=title, body=body)
            return Response({"message": "Service Updated", "data": serialized.data})
    return Response({"message": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)


# Manager Process Service
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def process_service_mgr(request):
    service = get_object_or_404(Service, pk=request.data.get('id'))
    if not request.data.get('name'):
        request.data['name'] = service.name
    if not request.data.get('description'):
        request.data['description'] = service.description
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        vd = serializer.validated_data
        serializer.update(instance=service, validated_data=vd)
        serialized = FullServiceSerializer(service)

        if service.state == "approved":
            # Notification For Tech
            fcm = service.worker.fcm_token
            title = "New Assignement"
            body = f"You Have A New Service Assignement: '{service.name}'"
            # print(title)
            # print(body)
            # print(fcm)
            sendFcm(fcm=fcm, title=title, body=body)
            # Notification For Client
            fcm = service.employee.fcm_token
            title = "Request Approved"
            body = f"Dear '{service.employee}': Your Service Request '{service.name}' Has Approved"
            # print(title)
            # print(body)
            # print(fcm)
            sendFcm(fcm=fcm, title=title, body=body)
            return Response({"message": "Service Approved", "data": serialized.data}, status=status.HTTP_200_OK)
        elif service.state == "rejected":
            # Notification For Client
            fcm = service.employee.fcm_token
            title = "Request Rejected"
            body = f"Dear '{service.employee}': Your Service Request '{service.name}' Has Rejected \nReason: {service.reason}"
            # print(title)
            # print(body)
            # print(fcm)
            sendFcm(fcm=fcm, title=title, body=body)
            return Response({"message": "Service Request Rejected", "data": serialized.data}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid State, Not In ['rejected','approved']"}, status=status.HTTP_400_BAD_REQUEST)


# Tech View Approved Services:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_approved_service_tech(request, id):
    service = Service.objects.filter(
        worker=id, state='approved')
    # serializer = ServiceSerializer(service, many=True)
    serializer = FullServiceSerializer(service, many=True)
    return Response({"service": serializer.data})


# Tech View Started Services:
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_started_service_tech(request, id):
    service = Service.objects.filter(
        worker=id, state='started')
    # serializer = ServiceSerializer(service, many=True)
    serializer = FullServiceSerializer(service, many=True)
    return Response({"service": serializer.data})


# Tech Process Service:
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def process_service_tech(request):
    service = get_object_or_404(Service, pk=request.data.get('id'))
    if not request.data.get('name'):
        request.data['name'] = service.name
    if not request.data.get('description'):
        request.data['description'] = service.description
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        vd = serializer.validated_data
        serializer.update(instance=service, validated_data=vd)
        serialized = ServiceSerializer(service)

        # Notification
        if service.state == 'started':
            fcm = service.employee.fcm_token
            title = "Service Process Started"
            body = f"Dear '{service.employee}': Your Service Request '{service.name}' Process Has Started"
            # print(title)
            # print(body)
            # print(fcm)
            sendFcm(fcm=fcm, title=title, body=body)
            return Response({"message": "Service Request Process Started", "data": serialized.data}, status=status.HTTP_200_OK)
        if service.state == 'ended':
            fcm = service.employee.fcm_token
            title = "Service Process Ended"
            body = f"Dear '{service.employee}': Your Service Request '{service.name}' Process Has Ended, Please Give Us Your Feedback"
            # print(title)
            # print(body)
            # print(fcm)
            sendFcm(fcm=fcm, title=title, body=body)
            return Response({"message": "Service Request Process Ended", "data": serialized.data}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


# Client Add Feedback:
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_feedback(request, *args, **kwargs):
    service = get_object_or_404(Service, pk=request.data.get('service'))
    manager = get_object_or_404(Employee, role__name='Manager')
    serializer = FeedbackSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        service.state = 'closed'
        service.save()
        # Notification
        fcm = manager.fcm_token
        title = "Feedback Added & Service Closed"
        body = f"Client '{service.employee}' Has Rated The Service '{service.name}'"
        # print(title)
        # print(body)
        # print(fcm)
        sendFcm(fcm=fcm, title=title, body=body)
        serialized = FullFeedbackSerializer(instance)
        return Response({"message": "Feedback Added & Service Closed", "data": serialized.data})
    return Response({"message": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)


# Manager Service Archive
class ArchiveServiceAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        services = Service.objects.filter(state="archived")
        # serializer = ServiceSerializer(services, many=True)
        serializer = FullServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        service = get_object_or_404(Service, pk=request.data.get('id'))
        if service.state == "closed":
            service.state = 'archived'
            service.save()
            return Response({"message": "Service Archived"}, status=status.HTTP_200_OK)
        if service.state == "archived":
            return Response({"message": "Service Already Archived"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Service isn't Closed, Can not be Archived"}, status=status.HTTP_400_BAD_REQUEST)


################
##  ViewSets  ##
################
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
    serializer_class = FullServiceSerializer
    # serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]


# Feedback Viewset
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FullFeedbackSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
