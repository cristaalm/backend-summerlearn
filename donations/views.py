# myApp/views.py

from django.shortcuts import render
from myApp.models import Donations, Bills
from donations.controllers.donationSerializers import DonationSerializer, BillsSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import datetime
from django.utils.timezone import now
from django.db.models import F, Q  # Asegúrate de incluir esta línea
from django.http import HttpResponse

# Importar la función de exportación a Excel
from .utils.excel.export_bills import export_bills_to_excel

###########################################################################################
class DonationsViews(viewsets.ModelViewSet):
    queryset = Donations.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='get-donations-by-week')
    def get_donations_by_week(self, request):
        user = request.user  # Obtiene el usuario autenticado

        if not user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)

        today = now().date()

        # Calcular inicio y fin de la semana actual (lunes a domingo)
        start_of_week = today - datetime.timedelta(days=today.weekday())  # Lunes es 0
        end_of_week = start_of_week + datetime.timedelta(days=6)  # Domingo es 6

        # Filtrar donaciones en la semana actual
        donations = Donations.objects.filter(
            donations_user=user,
            donations_date__range=[start_of_week, end_of_week]
        )

        donations_by_day = [0] * 7  # Array para las donaciones de lunes a domingo

        # Asignar las donaciones a los días correctos
        for donation in donations:
            day_of_week = donation.donations_date.weekday()  # Lunes = 0, Domingo = 6
            donations_by_day[day_of_week] += donation.donations_quantity

        return Response({
            "donations_by_day": donations_by_day,
            "total_donations": sum(donations_by_day)
        })

    @action(detail=False, methods=['get'], url_path='available-donations')
    def get_available_donations(self, request):
        # Filtrar donaciones que tienen fondos disponibles
        available_donations = Donations.objects.filter(
            Q(donations_spent__isnull=True) | Q(donations_spent__lt=F('donations_quantity'))
        )
        
        # Serializar las donaciones filtradas
        serializer = DonationSerializer(available_donations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


###########################################################################################
class BillsViews(viewsets.ModelViewSet):
    queryset = Bills.objects.all()
    serializer_class = BillsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=['get'], url_path='exportar-excel')
    def exportar_bills_excel(self, request):
        return export_bills_to_excel(self.get_queryset())
