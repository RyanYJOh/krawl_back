from rest_framework import serializers
from .models import Competitions_Master, WinnerContents_Detail, Likes_History

class CompetitionsM_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Competitions_Master
        fields = ['id', 'competition_id', 'url', 'raw_date', 'created_at', 'date_check', 'opinion', 'tag', 'del_yn']

class WinnerContentsD_Serializer(serializers.ModelSerializer):
    class Meta:
        model = WinnerContents_Detail
        fields = ['id', 'user_id', 'content_id', 'competition_id', 'point_id', 'awarded_at']

class LikesH_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Likes_History
        fields = ['id', 'user_id', 'content_id', 'del_yn']

'''
bookcake에서 가져온 tips
--------
A 모델의 a필드가, id가 아닌 string값으로 serialize되게 하려면

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