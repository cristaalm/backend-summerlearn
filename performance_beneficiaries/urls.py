from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import PerformanceBeneficiariesViewSet


# Configuración del Router
router = DefaultRouter()
router.register(r'performance-beneficiaries', PerformanceBeneficiariesViewSet, basename='erformance-beneficiaries')
urlpatterns = router.urls