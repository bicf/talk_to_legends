from rest_framework import serializers
from .models import Legend


class LegendSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='slug', read_only=True)

    class Meta:
        model = Legend
        fields = ['id', 'name', 'description', 'biography', 'lang']