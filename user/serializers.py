from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPoint_History, UserPoint_Master, UserProfile_Master
from rest_framework.serializers import ReadOnlyField

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'email', 'password']

class UserSerializer(serializers.ModelSerializer):
    # username = ReadOnlyField(source='author.username')
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {"password": {"write_only":True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        return user

class UserProfileM_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile_Master
        fields = ['id', 'user_id', 'nickname', 'profile_img']

class UserPointH_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint_History
        fields = ['id', 'user_id', 'point_id', 'change_date', 'change_point']

class UserPointM_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint_Master
        fields = ['id', 'user_id', 'point_id', 'total_point', 'last_updated_at']
