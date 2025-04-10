from rest_framework import serializers
from .models import HappinessRecord, MentalHealthRecord


class HappinessRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HappinessRecord
        fields = '__all__'

class MentalHealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentalHealthRecord
        fields = '__all__'