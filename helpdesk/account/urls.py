from django.urls import path
from .views import UserRegisterAPIView, ChangePasswordAPIView


urlpatterns = [
    # path('', RegisterAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('change-password/', ChangePasswordAPIView.as_view(),
         name='change_password')
]
