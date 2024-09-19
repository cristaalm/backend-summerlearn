from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AreasViewSet, ProgramsViewSet, ActivitiesViewSet, ObjectivesViewSet


# Configuración del Router
router = DefaultRouter()
router.register(r'areas', AreasViewSet, basename='areas')
router.register(r'programs', ProgramsViewSet, basename='programs')
router.register(r'activities', ActivitiesViewSet, basename='activities')
router.register(r'objectives', ObjectivesViewSet, basename='objectives')

urlpatterns = router.urls
