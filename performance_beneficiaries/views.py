from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from myApp.models import PerformanceBeneficiaries
from .serializers import PerformanceBeneficiariesSerializer

# Import the function to export the data to Excel
# from .utils.excel.programs.export_programs import export_programs_to_excel
# from .utils.pdf.programs.export_programs import export_programs_to_pdf
# from .utils.excel.activities.export_activities import export_activities_to_excel
# from .utils.pdf.activities.export_activities import export_activities_to_pdf

class PerformanceBeneficiariesViewSet(viewsets.ModelViewSet):
    queryset = PerformanceBeneficiaries.objects.all()
    serializer_class = PerformanceBeneficiariesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Area successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)