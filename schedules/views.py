from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from myApp.models import DaysActivities, Schedules
from .serializers import DaysActivitiesSerializer, SchedulesSerializer

class DaysActivitiesSerializer(viewsets.ModelViewSet):
    queryset = DaysActivities.objects.all()
    serializer_class = DaysActivitiesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Day successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
        
class SchedulesSerializer(viewsets.ModelViewSet):
    queryset = Schedules.objects.all()
    serializer_class = SchedulesSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            "message": "Day successfully created",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)