from rest_framework import serializers
from .models import UserPoint_History, UserPoint_Master, UserProfile_Master

class UserProfileM_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile_Master
        fields = ['id', 'user_id', 'nickname', 'profile_img']

class UserPointH_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint_History
        fields = ['id', 'user_id', 'point_id', 'received_at', 'amount_point']

class UserPointM_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint_Master
        fields = ['id', 'user_id', 'point_id', 'total_point', 'last_updated_at']
