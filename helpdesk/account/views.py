from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from rest_framework import status
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,)
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes

from .models import Profile
from .permissions import IsAdmin
from .serializers import ProfileSerializer, ChangePasswordSerializer

# import json

# class RegisterAPIView(CreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


@method_decorator(csrf_protect, name='dispatch')
class UserRegisterAPIView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAdmin,)
    authentication_classes = (
        SessionAuthentication,
        BasicAuthentication,
        TokenAuthentication
    )


@method_decorator(csrf_protect, name='dispatch')
class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(
                    serializer.validated_data.get('old_password')):
                return Response(
                    {'old_password': ['Неправильный пароль']},
                    status=status.HTTP_400_BAD_REQUEST
                )
            self.object.set_password(
                serializer.validated_data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Пароль успешно изменен',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response(
            {'message': 'Вы ввели не все данные.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    creds = {
        get_user_model().USERNAME_FIELD: username,
        'password': password
    }

    user = authenticate(**creds)
    if user is None:
        return Response(
            {'message': 'Неправильный логин или пароль'},
            status=status.HTTP_400_BAD_REQUEST
        )
    if user.is_active:
        login(request, user)
        return Response({
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Вход выполнен успешно!',
                'data': []
            })
    return Response(
        {'message': 'Пользователь неактивен'},
        status=status.HTTP_400_BAD_REQUEST,
    )
