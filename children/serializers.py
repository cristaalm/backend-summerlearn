from rest_framework import serializers
from myApp.models import Children


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
        return representation