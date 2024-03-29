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

        ## Likes_Master 업데이트
        try:
            this_likeM = Likes_Master.objects.get(content_id=content_id)

            ## 그 전에, 이 유저가 이미 like를 했는지 확인
            try:
                ## 이미 좋아요 했음
                this_likeH = Likes_History.objects.filter(user_id=user_id, content_id=content_id, del_yn=False)
                # filter를 쓰니, 오브젝트가 없어도 쿼리셋을 리턴함 (빈 쿼리셋)
                if len(this_likeH) != 0:
                    return JsonResponse({'rescode' : 2})
                elif len(this_likeH) == 0:
                    this_likeM.count_like += 1
                    this_likeM.save()
            ## 좋아요 하지 않았음
            except ObjectDoesNotExist:
                this_likeM.count_like += 1
                this_likeM.save()

        ## Likes_Master에 오브젝트가 없다면, 새로 생성해주기
        except ObjectDoesNotExist:
            new_likeM = Likes_Master.objects.create(
                content_id = content_id,
                count_like = 1
            )

        ## Likes_History에 추가
        new_likeH = Likes_History.objects.create(
            user_id = user_id,
            content_id = content_id
        )

        return JsonResponse({'rescode' : 1})
    
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
        this_content = Contents_Detail.objects.get(id=pk)
        
        this_likeM = Likes_Master.objects.get(content_id=this_content)

        ## 현재 request.auth.user가 이 포스트의 주인인가?
        try:
            ## 이 사람이 여기에 좋아요를 했나?
            this_likeH = Likes_History.objects.get(user_id=request.auth.user, content_id=this_content, del_yn=False)
            this_likeH.delete()

            ## Likes_Master에서는 지움
            this_likeM.count_like = this_likeM.count_like - 1
            this_likeM.save()

            return JsonResponse({'message' : '사실 안 좋아요!!!!!'})
        
        except ObjectDoesNotExist:
            return JsonResponse({'message' : '왜 남의 좋아요를 지우려고 하냐 ㅡㅡ'})

@api_view(['GET'])
@permission_classes((AllowAny,))
def getAllPosts(request):
    all_posts = Contents_Detail.objects.filter(date_check=True, del_yn=False).order_by('-created_at')
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

        # 좋아요 한 유저 추가
        likers = Likes_History.objects.filter(content_id=this_data[i]['id'], del_yn=False).values_list('user_id', flat=True)
        
        this_data[i]['likers'] = list(likers)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny,))
def getPostsFiltered(request, tag):
    filtered_posts = Contents_Detail.objects.filter(date_check=True, del_yn=False, tag__contains=tag).order_by('-created_at')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(filtered_posts, request)

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

        # 좋아요 한 유저 추가
        likers = Likes_History.objects.filter(content_id=this_data[i]['id'], del_yn=False).values_list('user_id', flat=True)
        
        this_data[i]['likers'] = list(likers)

    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny,))
def getThisPost(request, pk):
    this_post = Contents_Detail.objects.get(id=pk)
    serializer = ContentsD_Serializer(this_post)
    this_data = serializer.data
    
    ## Likes와 댓글
    ## Likes
    try:
        this_post_likes = Likes_Master.objects.get(content_id=this_post)
        this_data['likes'] = this_post_likes.count_like

    except ObjectDoesNotExist:
        this_data['likes'] = 0
    
    ## Likers
    likers = Likes_History.objects.filter(content_id=this_data['id'], del_yn=False).values_list('user_id', flat=True)
        
    this_data['likers'] = list(likers)

    ## Comments
    try:
        this_post_comments = Comments_Master.objects.filter(content_id=this_post, del_yn=False).values().order_by('-created_at')
        list__this_post_comments = list(this_post_comments)
        
        for i in range(0, len(list__this_post_comments)):
            comment_author = User.objects.get(id=list__this_post_comments[i]['user_id_id'])
            this_userprofile = UserProfile_Master.objects.get(user_id=comment_author)

            nickname =  this_userprofile.nickname
            profile_img =  this_userprofile.profile_img.url
            
            list__this_post_comments[i]['current_user'] = {
                'nickname' : nickname,
                'profile_img' : profile_img
            }
    except ObjectDoesNotExist:
        list__this_post_comments = []  
    
    this_data['comments'] = list__this_post_comments

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
    popular_likes = Likes_Master.objects.order_by('-count_like')[:10].values('content_id')

    list__popular_contents_id = []
    for i in range(0, len(popular_likes)):
        list__popular_contents_id.append(popular_likes[i]['content_id'])

    popular_contents = Contents_Detail.objects.filter(date_check=True, del_yn=False, id__in=list__popular_contents_id)
    serializer = ContentsD_Serializer(popular_contents, many=True)

    return Response(serializer.data, status=200)