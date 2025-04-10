from rest_framework import serializers
from .models import HappinessRecord

class HappinessRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HappinessRecord
        fields = '__all__'