from rest_framework import serializers
from myApp.models import Children, PerformanceBeneficiaries


class ChildrensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Children
        fields = '__all__'
        read_only_fields = ('children_id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['children_user'] = {
            'id': instance.children_user.id,
            'name': instance.children_user.name,
        }

        representation['children_grade'] = {
            'id': instance.children_grade.grades_id,
            'description': instance.children_grade.grades_description,
        }
        return representation
 

class PerformanceBeneficiariesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceBeneficiaries
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['performance_beneficiaries_subscription'] = {
            'performance_beneficiaries_id': instance.performance_beneficiaries_id,
            'subscriptions_children_activity': {
                'activities_id': instance.performance_beneficiaries_subscription.subscriptions_children_activity.activities_id,
                'activities_name': instance.performance_beneficiaries_subscription.subscriptions_children_activity.activities_name,
            },
            'subscriptions_children_child': {
                'children_id': instance.performance_beneficiaries_subscription.subscriptions_children_child.children_id,
                'children_name': instance.performance_beneficiaries_subscription.subscriptions_children_child.children_name,
            }
        }
        return representation