from rest_framework import serializers
from myApp.models import PerformanceBeneficiaries


class PerformanceBeneficiariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceBeneficiaries
        fields = '__all__'
        read_only_fields = ('performance_beneficiaries_id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['performance_beneficiaries_subscription'] = {
            'id': instance.performance_beneficiaries_subscription.subscriptions_children_id,
            'child': instance.performance_beneficiaries_subscription.subscriptions_children_child.children_name,
            'activity': instance.performance_beneficiaries_subscription.subscriptions_children_activity.activities_name,
        }
        return representation

