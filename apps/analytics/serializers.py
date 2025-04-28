from rest_framework import serializers
from .models import MergedDataRecord

class MergedDataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MergedDataRecord
        fields = '__all__'