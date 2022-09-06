from rest_framework import serializers

from .models import *


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    def save(self, *args, **kwargs):
        if self.instance is not None:
            if len(self.validated_data['employees']) > self.validated_data['max_amount']:
                raise QuantityLimit(f"In department cannot work more then {self.validated_data['max_amount']} workers!")
            return super().save(*args, **kwargs)

        if len(self.validated_data['employees']) > self.validated_data['max_amount']:
            raise QuantityLimit(f"In department cannot work more then {self.validated_data['max_amount']} workers!")
        return super().save(*args, **kwargs)


class HistoryVacationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryVacation
        fields = '__all__'

    # def save(self, *args, **kwargs):
    #     departments = Department.objects.filter(employees__id=self.validated_data['employee_id'].id)
    #     for department in departments:
    #         breakpoint()
    #         if len(Employee.objects.filter(departments__id=department.id)) > 5:
    #             raise QuantityLimit('Currently on vacation are 5 employees')
    #         return super().save(*args, **kwargs)


class ReportVacationSerializer(serializers.Serializer):
    days = serializers.DurationField()
    employee_id = serializers.IntegerField()


class QuantityLimit(Exception):
    pass
