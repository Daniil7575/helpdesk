# from django.shortcuts import render
from django.contrib.auth.models import User
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Profile
from .permissions import IsAdmin
from .serializers import ProfileSerializer, ChangePasswordSerializer

# class RegisterAPIView(CreateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


class UserRegisterAPIView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAdmin,)


class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

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
