from rest_framework import serializers
from .models import File, Result, CalculatePath


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class CalculatePathSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculatePath
        fields = '__all__'
