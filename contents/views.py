from http.client import HTTPResponse
from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from votes.models import Competitions_Master
from user.models import UserPoint_Master, UserPoint_History
from votes.models import Points_Master
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from contents.serializers import ContentsD_Serializer, LikesH_Serializer, LikesM_Serializer
from .models import Contents_Detail, WinnerContents_Detail, Likes_History, Likes_Master
from django.utils import timezone
from datetime import datetime, date
from django.core.exceptions import ObjectDoesNotExist

# json parsing을 위한 임포트
import io, json
from rest_framework.parsers import JSONParser

# Create your views here.
now = timezone.now()
string__today = str(now).split()[0]
today = datetime.strptime(string__today, '%Y-%m-%d').date()

@api_view(['POST'])
@permission_classes((AllowAny,))
def post(request):
    if request.method == 'GET':
        return HTTPResponse(status=200)
    elif request.method == 'POST':
        ## 콘텐츠 POST
        posted = request.data

        user_id = User.objects.get(id=posted['user_id'])
        competition_id = Competitions_Master.objects.get(id=posted['competition_id'])

        new_content = Contents_Detail.objects.create(
            user_id = user_id,
            competition_id = competition_id,
            url = posted['url'],
            raw_date = posted['raw_date'],
            date_check = posted['date_check'],
            opinion = posted['opinion'],
            tag = posted['tag']
        )
        new_content.save()
        serializer = ContentsD_Serializer(data=request.data) # many=True
        
        ## 유저 포인트 차감
        # 게시글 등록에 해당하는 point_id
        this_point = Points_Master.objects.get(id=7)

        # UserPoint_M에서 -2점 차감
        try : 
            this_userPointM = UserPoint_Master.objects.get(user_id=user_id)
            this_userPointM.total_point = this_userPointM.total_point + this_point.get_point
            this_userPointM.last_updated_at = today
            this_userPointM.save()
        except ObjectDoesNotExist:
            this_userPointM = UserPoint_Master.objects.create(
            user_id = user_id,
            point_id = this_point,
            total_point = this_point.get_point,
            last_updated_at = today
        )

        # UserPoint_H에 기록
        this_userPointH = UserPoint_History.objects.create(
            user_id = user_id,
            point_id = this_point,
            change_point = this_point.get_point
        )
        
        if serializer.is_valid():    
            return Response(serializer.data, status=200)
    

@api_view(['GET'])
@permission_classes((AllowAny,))
def winnerContent(request):
    return

@api_view(['POST'])
@permission_classes((AllowAny,))
def postLike(request):
    if request.method == 'GET':
        return HTTPResponse(status=200)
    elif request.method == 'POST':
        ## Like
        posted = request.data

        user_id = User.objects.get(id=posted['user_id'])
        content_id = Contents_Detail.objects.get(id=posted['content_id'])

        serializer = LikesM_Serializer(data=request.data) # many=True

        ## Likes_Master 업데이트
        # 그 전에, Likes_Master 오브젝트가 없다면 생성해주기
        try:
            this_likeM = Likes_Master.objects.get(content_id=content_id)
            this_likeM.count_like += 1
            this_likeM.save()
        except ObjectDoesNotExist:
            new_likeM = Likes_Master.objects.create(
                content_id = content_id,
                count_like = 1
            )

        ## Likes_History에 추가
        new_like = Likes_History.objects.create(
            user_id = user_id,
            content_id = content_id
        )

        if serializer.is_valid():    
            return Response(serializer.data, status=200)
    

@api_view(['GET', 'DELETE'])
@permission_classes((AllowAny,))
def getDelLike(request, pk):
    if request.method == 'GET':
        this_like = Likes_History.objects.get(id=pk)
        serializer = LikesH_Serializer(
            this_like,
            )
        return Response(serializer.data, status=200)

    elif request.method == 'DELETE':
        ## Likes_Master에서는 지움
        this_content = Likes_History.objects.get(id=pk).content_id.id
        
        this_likeM = Likes_Master.objects.get(content_id=this_content)
        this_likeM.count_like = this_likeM.count_like - 1
        this_likeM.save()
        
        ## Likes_History에서는 del_yn만 변경
        this_likeH = Likes_History.objects.get(id=pk)
        this_likeH.del_yn = True
        this_likeH.save()
