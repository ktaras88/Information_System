from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from company.views import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/v1/persons/', PersonAPIView.as_view()),
    path('api/v1/persons/<int:pk>/', PersonAPIDetailView.as_view()),
    path('api/v1/employees/', EmployeeAPIView.as_view()),
    path('api/v1/employees/<int:pk>/', EmployeeAPIDetailView.as_view()),
    path('api/v1/employees/<int:pk>/vacations/', EmployeeVacationAPIView.as_view()),
    path('api/v1/positions/', PositionAPIView.as_view()),
    path('api/v1/positions/<int:pk>/', PositionAPIDetailView.as_view()),
    path('api/v1/departments/', DepartmentAPIView.as_view()),
    path('api/v1/departments/<int:pk>/', DepartmentAPIDetailView.as_view()),
    path('api/v1/departments/<int:pk>/employees/', DepartmentEmployeeAPIView.as_view()),
    path('api/v1/reports/', ReportsAPIView.as_view()),
    path('api/v1/reports/vacations/', ReportsVacationsAPIView.as_view()),
]
