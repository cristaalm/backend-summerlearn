from rest_framework.routers import DefaultRouter
from donations.views import DonationsViews, BillsViews
from django.urls import path, include

router = DefaultRouter()

router.register(r'donations', DonationsViews, basename='donations')
router.register(r'bills', BillsViews, basename='bills')

urlpatterns = [
    path('', include(router.urls)),  # Rutas CRUD para Donations 
    path('bills/exportar-excel/', BillsViews.as_view({'get': 'exportar_bills_excel'}), name='exportar_bills_excel'),
    path('bills/exportar-pdf/', BillsViews.as_view({'get': 'exportar_bills_pdf'}), name='exportar_bills_pdf'),
    path('donations/exportar-excel/', DonationsViews.as_view({'get': 'exportar_donations_excel'}), name='exportar_donations_excel'),
]