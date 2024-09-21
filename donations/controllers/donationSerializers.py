from rest_framework import serializers
from myApp.models import Donations, Bills


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = '__all__'
        READ_ONLY_FIELDS = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['donations_user'] = {
            'id': instance.donations_user.id,
            'name': instance.donations_user.name,
        }
        return representation   

#########################################################################################################
class BillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bills
        fields = '__all__'
        READ_ONLY_FIELDS = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['bills_donations'] = {
            'id': instance.bills_donations.donations_user.id,
            'name': instance.bills_donations.donations_user.name,
        }
        return representation