from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import *
from .serializers import *


def index(request):
    return render(request, "backend/index.html")


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
    department = get_object_or_404(Department, id=id)
    deptserializer = DepartmentSerializer(department)
    return Response({"department": deptserializer.data, "name": deptserializer.data['name']})
