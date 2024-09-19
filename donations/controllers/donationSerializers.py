from rest_framework import serializers
from myApp.models import Donations, Bills


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = '__all__'
        READ_ONLY_FIELDS = ['id', 'created_at', 'updated_at']


#########################################################################################################
class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = '__all__'
        READ_ONLY_FIELDS = ['id', 'created_at', 'updated_at']