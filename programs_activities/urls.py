from django.urls import include, path
from rest_framework.routers import DefaultRouter
from programs_activities.serializers import AreasSerializer
from accounts.models import Areas
from .views import AreasViewSet, ProgramsViewSet


# Configuración del Router
router = DefaultRouter()
router.register(r'areas', AreasViewSet, basename='Áreas')
router.register(r'programs', ProgramsViewSet, basename='Programas')

urlpatterns = router.urls
