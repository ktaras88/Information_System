from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=20)
    second_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    passport = models.CharField(max_length=10)
    birthday = models.DateField()
    place_birthday = models.CharField(max_length=20)
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name + ' ' + self.second_name


class Position(models.Model):
    position = models.CharField(max_length=20)
    rate = models.IntegerField()
    vacation_days = models.IntegerField()

    def __str__(self):
        return self.position


class Employee(models.Model):
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    employment_date = models.DateField()
    fired_date = models.DateField()
    head_officer = models.BooleanField(default=False)


class Department(models.Model):
    employees = models.ManyToManyField(Employee, related_name='departments')
    name = models.CharField(max_length=20)
    abbreviation = models.CharField(max_length=10)
    max_amount = models.IntegerField(default=20)

    def __str__(self):
        return self.name


class HistoryVacation(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    finish_date = models.DateField()
