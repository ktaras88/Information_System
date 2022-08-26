from django.contrib import admin
from .models import Person, Position, Employee, Department, HistoryVacation


admin.site.register((Person, Position, Employee, Department, HistoryVacation))
