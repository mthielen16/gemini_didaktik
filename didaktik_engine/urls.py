from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.ki_test_view, name='ki_test'),
]