from http.client import HTTPResponse
from django.shortcuts import render
from rest_framework.response import Response
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from user.serializers import UserPointM_Serializer
from votes.models import Competitions_Master
from user.models import UserPoint_Master, UserPoint_History, UserProfile_Master
from votes.models import Points_Master
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from contents.serializers import ContentsD_Serializer, LikesH_Serializer, LikesM_Serializer, CommentsM_Serializer
from .models import Comments_Master, Contents_Detail, WinnerContents_Detail, Likes_History, Likes_Master
from django.utils import timezone
from datetime import datetime, date
from django.core.exceptions import ObjectDoesNotExist
from .pagination import PostPageNumberPagination
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator

# json parsing을 위한 임포트
import io, json
from rest_framework.parsers import JSONParser

# Create your views here.
now = timezone.now()
string__today = str(now).split()[0]
today = datetime.strptime(string__today, '%Y-%m-%d').date()

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post(request):
    if request.method == 'GET':
        return HTTPResponse(status=200)
    elif request.method == 'POST':
        ## 포스트 진행
        posted = request.data

        user_id = request.auth.user
        # user_id = User.objects.get(id=posted['user_id'])
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
@permission_classes((IsAuthenticated,))
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
@permission_classes((IsAuthenticated,))
def getDelLike(request, pk):
    if request.method == 'GET':
        this_like = Likes_History.objects.get(id=pk)
        serializer = LikesH_Serializer(
            this_like,
            )
        return Response(serializer.data, status=200)

    elif request.method == 'DELETE':
        this_content = Likes_History.objects.get(id=pk).content_id.id
        this_likeM = Likes_Master.objects.get(content_id=this_content)

        ## 현재 request.auth.user가 이 포스트의 주인인가?
        if this_likeM.user_id == request.auth.user:
            ## Likes_Master에서는 지움
            this_likeM.count_like = this_likeM.count_like - 1
            this_likeM.save()
            
            ## Likes_History에서는 del_yn만 변경
            this_likeH = Likes_History.objects.get(id=pk)
            this_likeH.del_yn = True
            this_likeH.save()

            return JsonResponse({'message' : '사실 안좋아요지롱!'})
        else:
            return JsonResponse({'message' : '내 좋아요만 지울 수 있음요'})

@api_view(['GET'])
@permission_classes((AllowAny,))
def getAllPosts(request):
    all_posts = Contents_Detail.objects.filter(date_check=True).order_by('-created_at')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(all_posts, request)

    serializer = ContentsD_Serializer(result_page, many=True)

    this_data = serializer.data
    for i in range(0,len(this_data)):
        this_user = User.objects.get(id=this_data[i]['user_id'])
        # nickname, profile_img 추가
        this_userprofile = UserProfile_Master.objects.get(user_id=this_user)
        nickname =  this_userprofile.nickname
        profile_img =  this_userprofile.profile_img.url
        
        this_data[i]['current_user'] = {
            'nickname' : nickname,
            'profile_img' : profile_img
        }

        # total_point 추가
        try : 
            total_point = UserPoint_Master.objects.get(user_id=this_user).total_point
        except :
            total_point = 0
        
        this_data[i]['current_user']['total_point'] = total_point
        
    ## 현재 컴페티션 아이디에서 남은 기간 -> 나중에..

    # return Response(serializer.data, status=200)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny,))
def getThisPost(request, pk):
    this_post = Contents_Detail.objects.get(id=pk)
    serializer = ContentsD_Serializer(this_post)
    this_data = serializer.data
    
    ## Likes와 댓글
    this_post_likes = Likes_Master.objects.get(content_id=this_post)
    # this_post_comments = 

    this_data['likes'] = this_post_likes.count_like
    
    ## 그 외 user info
    author_profile = UserProfile_Master.objects.get(user_id=this_post.user_id)
    nickname = author_profile.nickname
    profile_img = author_profile.profile_img.url
    
    this_data['nickname'] = nickname
    this_data['profile_img'] = profile_img
    
    return JsonResponse(this_data, status=200)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def postComment(request):
    if request.method == 'GET':
        return HTTPResponse(status=200)
    elif request.method == 'POST':
        posted = request.data

        # user_id = User.objects.get(id=posted['user_id'])
        user_id = request.auth.user
        content_id = Contents_Detail.objects.get(id=posted['content_id'])
        
        new_comment = Comments_Master.objects.create(
            user_id = user_id,
            content_id = content_id,
            body = posted['body']
        )
        new_comment.save()
        serializer = CommentsM_Serializer(data=request.data)

        if serializer.is_valid():    
            return Response(serializer.data, status=200)
    
@api_view(['GET'])
@permission_classes((AllowAny,))
def getComments(request, pk):
    this_content = Contents_Detail.objects.get(id=pk)
    this_comment = Comments_Master.objects.filter(content_id=this_content, del_yn=False).order_by('-created_at')
    serializer = CommentsM_Serializer(this_comment, many=True)
    
    this_data = serializer.data

    for i in range(0, len(this_data)):
        comment_author = User.objects.get(id=this_data[i]['user_id'])
        this_userprofile = UserProfile_Master.objects.get(user_id=comment_author)

        nickname =  this_userprofile.nickname
        profile_img =  this_userprofile.profile_img.url
        
        this_data[i]['current_user'] = {
            'nickname' : nickname,
            'profile_img' : profile_img
        }

    return Response(serializer.data, status=200)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delComment(request, pk):
    this_comment = Comments_Master.objects.get(id=pk)
    if this_comment.user_id == request.auth.user:
        this_comment.del_yn = True
        this_comment.save()
    
        return JsonResponse({'message' : '댓글 정상적으로 삭제 됨'})
    else:
        return JsonResponse({'message' : '남의 댓글을 왜 지우냐 ㅡㅡ'})

@api_view(['GET'])
@permission_classes((AllowAny,))
def getPopular(request):
    popular_likes = Likes_Master.objects.order_by('-count_like')[:5].values('content_id')

    list__popular_contents_id = []
    for i in range(0, len(popular_likes)):
        list__popular_contents_id.append(popular_likes[i]['content_id'])

    popular_contents = Contents_Detail.objects.filter(date_check=True, id__in=list__popular_contents_id)
    serializer = ContentsD_Serializer(popular_contents, many=True)

    return Response(serializer.data, status=200)