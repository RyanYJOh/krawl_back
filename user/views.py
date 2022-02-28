from http.client import ImproperConnectionState
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from user.models import UserPoint_History, UserPoint_Master, UserProfile_Master
from votes.models import Points_Master
from .serializers import UserPointM_Serializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import datetime, date
import json

## 회원가입 시 token 생성을 위한 임포트
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

now = timezone.now()
string__today = str(now).split()[0]
today = datetime.strptime(string__today, '%Y-%m-%d').date()

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        '회원가입' : 'accounts/register',
    }
    return Response(api_urls)

@csrf_exempt
@api_view(['GET'])
@permission_classes((AllowAny,))
def account_list(request): ## 게정 전체 조회(GET)
    query_set = User.objects.all()
    serializer = UserSerializer(query_set, many=True)
    return Response(serializer.data) # safe=False

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request): # 회원가입 (POST)
    data = JSONParser().parse(request)

    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        this_user = User.objects.get(username=serializer.data['username'])

        ## UserProfile_Master 생성
        this_userProfileM = UserProfile_Master.objects.create(
            user_id = this_user
        )
        ## 가입 시 유저에게 포인트 증정
        this_user = User.objects.get(username=serializer.data['username'])
        this_userPointM = UserPoint_Master.objects.create(
            user_id = this_user,
            point_id = Points_Master.objects.get(id=6),
            total_point = Points_Master.objects.get(id=6).get_point,
            last_updated_at = today
        )

        this_userPointH = UserPoint_History.objects.create(
            user_id = this_user,
            point_id = Points_Master.objects.get(id=6),
            change_date = today,
            change_point = Points_Master.objects.get(id=6).get_point
        )
        
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

## 회원가입 시 token 생성
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((AllowAny,))
def account(request, pk): ## 특정계정 조회(GET), 수정(PUT), 삭제(DELETE)

    obj = User.objects.get(pk=pk)

    if request.method == 'GET':
        serializer = UserSerializer(obj)
        return Response(serializer.data) # safe=False

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)

@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None or username is None:
        return Response({'error': 'Please provide both username and password'},
                        status=400)

	# 여기서 authenticate로 유저 validate
    user = authenticate(username=username, email=email, password=password)
    
    if not user:
        return Response({'error': 'Invalid credentials'}, status=404)

	# user 로 토큰 발행
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=200)

## logout은?


## UserPoint 
@api_view(['GET', 'PUT'])
@permission_classes((AllowAny,))
def getPutUserPoint(request, pk):
    this_user = User.objects.get(id=pk)
    this_userpoint = UserPoint_Master.objects.get(user_id=this_user)

    if request.method == 'GET':
        serializer = UserPointM_Serializer(this_userpoint)
        return Response(serializer.data) # safe=False

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserPointM_Serializer(this_userpoint, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes((AllowAny,))
def getRankings(request):
    ranking = UserPoint_Master.objects.all().order_by('-total_point').values('user_id')[:3]
    ranker_wrapper = []

    for i in range(0, len(ranking)):
        ranker = {}
        user_id = ranking[i]['user_id']
        print('user id : ', user_id)
        this_user = UserProfile_Master.objects.get(id=user_id)
        this_userPoint = UserPoint_Master.objects.get(user_id=user_id).total_point
        ranker['nickname'] = this_user.nickname
        ranker['profile_img'] = this_user.profile_img.url
        ranker['user_id'] = user_id
        ranker['user_point'] = this_userPoint
        ranker_wrapper.append(ranker)
    print(ranker)
    json.dumps(ranker)
        
    return Response(ranker_wrapper, status=200)

@api_view(['GET'])
@permission_classes((AllowAny,))
def getLoggedIn(request):
    ## 토큰이 있는지 먼저 보고
    # 있으면
    # 토큰으로 this_user 가져옴. 이 this_user의 id로 UserProfile_Master에서 이름과 프사,
    # UserPoint_Master에서 total_point 가져오면 됨
    # 없으면
    ranking = UserPoint_Master.objects.all().order_by('total_point')[:5].values('user_id')
    ranker_wrapper = []
    for i in range(0, len(ranking)):
        ranker = {}
        user_id = ranking[i]['user_id']
        print('user id : ', user_id)
        this_user = UserProfile_Master.objects.get(id=user_id)
        this_userPoint = UserPoint_Master.objects.get(user_id=user_id).total_point
        ranker['nickname'] = this_user.nickname
        ranker['profile_img'] = this_user.profile_img.url
        ranker['user_id'] = user_id
        ranker['user_point'] = this_userPoint
        ranker_wrapper.append(ranker)
    print(ranker)
    json.dumps(ranker)
        
    return Response(ranker_wrapper, status=200)
