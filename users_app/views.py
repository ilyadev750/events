from django.shortcuts import render
from .models import Token, EventRegistration
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated 
from django.contrib.auth import authenticate, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, UserEventSerializer, EventRegistrationSerializer
from rest_framework import viewsets


class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return EventRegistration.objects.filter(user_id=user)

    def create(self, request, *args, **kwargs):
        serializer = EventRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'event_registration': serializer.data})



@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"Ошибка": "Неверное имя пользователя или пароль"})
        
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })

        token = Token.objects.create(user_id=user)
        token.refresh_token = str(refresh)
        token.access_token = str(refresh.access_token)
        token.save()
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'Ошибка': 'Необходим Refresh токен'})
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            token = Token.objects.get(refresh_token=refresh_token)
            token.delete()

        except Exception:
            return Response({'Ошибка': 'Неверный Refresh токен'})
        return Response({'Успех': 'Выход из системы произведен'})