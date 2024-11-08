from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth.models import User
from .models import *
from .serializers import *


def index(request):
    return render(request, "backend/index.html")


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
    return Response({"token": token.key, "user": emp_serializer.data, "sess": session_hash})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def log_out(request):
    # employee = get_object_or_404(Employee, username=request.data['username'])
    # token = Token.objects.get(user=employee)
    # token.delete()
    request.user.auth_token.delete()
    return Response({"Details": "Logged Out!"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    employee = get_object_or_404(Employee, username=request.data['username'])
    deptserializer = DepartmentSerializer(employee.department)
    return Response({"department": deptserializer.data['name']})


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
@api_view(['GET'])
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
@permission_classes([IsAuthenticated, IsAdminUser])
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


# Feedback:
