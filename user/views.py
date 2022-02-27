from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

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
        print(serializer)
        print('##########', serializer.data)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

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

@csrf_exempt
@api_view(['POST'])
def logind(request):
    user = authenticate(username=request.data['id'], password=request.data['password'])
    if user is not None:
        token = Token.objects.get(user=user)
        return Response({"Token": token.key})
    else:
        return Response(status=401)