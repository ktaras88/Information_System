from django.shortcuts import render
from rest_framework import generics

from .models import *
from .serializers import *


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


class EmployeeVacationAPIView(generics.ListCreateAPIView):
    queryset = HistoryVacation.objects.all()
    serializer_class = HistoryVacationSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return HistoryVacation.objects.filter(employee_id=pk)


class DepartmentAPIView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class HistoryVacationAPIView(generics.ListAPIView):
    queryset = HistoryVacation.objects.all()
    serializer_class = HistoryVacationSerializer
