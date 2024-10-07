from rest_framework import serializers
from myApp.models import SubscriptionsChildren,SubscriptionsVolunteer

class SubscriptionsChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionsChildren
        fields = '__all__'
        read_only_fields = ('subscriptions_children_id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subscriptions_children_activity'] = {
            'id': instance.subscriptions_children_activity.activities_id,
            'name': instance.subscriptions_children_activity.activities_name,
        }
        representation['subscriptions_children_child'] = {
            'id': instance.subscriptions_children_child.children_id,
            'name': instance.subscriptions_children_child.children_name,
        }
        return representation

class SubscriptionsVolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionsVolunteer
        fields = '__all__'
        read_only_fields = ('subscriptions_volunteer_id',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subscriptions_volunteer_activity'] = {
            'id': instance.subscriptions_volunteer_activity.activities_id,
            'name': instance.subscriptions_volunteer_activity.activities_name,
        }
        representation['subscriptions_volunteer_user'] = {
            'id': instance.subscriptions_volunteer_user.id,
            'name': instance.subscriptions_volunteer_user.name,
        }
        return representation