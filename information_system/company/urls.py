from django.urls import path

from .views import *

urlpatterns = [
    path('personlist/', PersonAPIView.as_view()),
    path('personlist/<int:pk>/', PersonAPIDetailView.as_view()),
]
