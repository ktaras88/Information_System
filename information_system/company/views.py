from django.shortcuts import render
from rest_framework import generics

from .models import Person, Position, Employee, Department, HistoryVacation
from .serializers import PersonSerializer, PositionSerializer, EmployeeSerializer, DepartmentSerializer, \
    HistoryVacationSerializer


class PersonAPIView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PersonAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class PositionAPIView(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class EmployeeAPIView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class DepartmentAPIView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class HistoryVacationAPIView(generics.ListCreateAPIView):
    queryset = HistoryVacation.objects.all()
    serializer_class = HistoryVacationSerializer


class HistoryVacationAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HistoryVacation.objects.all()
    serializer_class = HistoryVacationSerializer
