from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DaysActivitiesSerializer, SchedulesViewSet, DaysViewSet

# Configuración del Router
router = DefaultRouter()
router.register(r'days-activities', DaysActivitiesSerializer, basename='days-activities')
router.register(r'days', DaysViewSet, basename='days')
router.register(r'schedules', SchedulesViewSet, basename='schedules')

urlpatterns = router.urls