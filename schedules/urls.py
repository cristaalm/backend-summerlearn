from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DaysActivitiesSerializer, SchedulesSerializer

# Configuración del Router
router = DefaultRouter()
router.register(r'days', DaysActivitiesSerializer, basename='days')
router.register(r'schedules', SchedulesSerializer, basename='schedules')

urlpatterns = router.urls