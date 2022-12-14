import datetime

from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Person, Position, Employee, Department, HistoryVacation
from .serializers import PersonSerializer, PositionSerializer, EmployeeSerializer, DepartmentSerializer, \
    HistoryVacationSerializer, ReportVacationSerializer, ReportsSalarySerializer


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


class ReportsAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        reports = {
            'reports': [
                'List of employees of the departments',
                'List of days spent on vacation for each employee',
                'List of employees with position and rate',
                'List of departments with an indication of the head of department and the number of employees',
                'List of salaries for employees'
            ]
        }
        return Response(reports)


class DepartmentEmployeeAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Department.objects.get(id=pk).employees.all()


class ReportsVacationsAPIView(generics.ListAPIView):
    queryset = HistoryVacation.objects.values('employee_id').annotate(days=Sum(F('finish_date')-F('start_date')))
    serializer_class = ReportVacationSerializer


class ReportsSalaryAPIView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        total = []
        for employee in employees:
            salary_info = {}
            experience = datetime.date.today() - employee.employment_date
            if experience.days >= 365:
                salary = employee.position_id.rate * (1 + (experience.days//365) * 0.012)
            else:
                salary = employee.position_id.rate
            salary_info['name'] = employee.person_id.first_name+' '+employee.person_id.second_name
            salary_info['position'] = employee.position_id.position
            salary_info['rate'] = employee.position_id.rate
            salary_info['salary'] = salary
            total.append(salary_info)
        return Response(ReportsSalarySerializer(total, many=True).data)
