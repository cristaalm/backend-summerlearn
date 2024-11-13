from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ChildrensViewSet, PerformanceBeneficiariesViewSet


# Configuración del Router
router = DefaultRouter()
router.register(r'childrens', ChildrensViewSet, basename='childrens')
router.register(r'performance-beneficiaries', PerformanceBeneficiariesViewSet, basename='performance-beneficiaries')


urlpatterns = router.urls
