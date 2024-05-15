from rest_framework import serializers
from new_api.models import CRMLed, MASSlm


class CRMLedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRMLed
        fields = '__all__'


class MASSlmSerializer(serializers.ModelSerializer):
    class Meta:
        model = MASSlm
        fields = '__all__'
