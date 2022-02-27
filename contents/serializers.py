from rest_framework import serializers
from .models import Contents_Detail, WinnerContents_Detail, Likes_History, Likes_Master

class ContentsD_Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contents_Detail
        fields = ['id', 'user_id', 'competition_id', 'url', 'raw_date', 'created_at', 'date_check', 'opinion', 'tag', 'del_yn']

class WinnerContentsD_Serializer(serializers.ModelSerializer):
    class Meta:
        model = WinnerContents_Detail
        fields = ['id', 'user_id', 'content_id', 'competition_id', 'point_id', 'awarded_at']

class LikesH_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Likes_History
        fields = ['id', 'user_id', 'content_id', 'del_yn']

class LikesM_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Likes_Master
        fields = ['id', 'content_id', 'count_like']

'''
bookcake에서 가져온 tips
--------
A 모델의 a필드가, id가 아닌 값으로 serialize되게 하려면

a = serializers.StringRelatedField(many=True)

class Meta: ...

-------
foreign key에서 특정 필드 보여주기
source_title = serializers.SerializerMethodField()

class Meta: ...

def get_source_title(self, obj):
    this_title = self.context['cake'].source.title
    this_author = self.context['cake'].source.author
    return this_author + this_title
'''