from rest_framework import serializers
from .models import Points_Master, Competitions_Master

class PointsM_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Points_Master
        fields = ['id', 'point_name', 'get_point']

class CompetitionsM_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Competitions_Master
        fields = ['id', 'point_id', 'starts_at', 'ends_at']



