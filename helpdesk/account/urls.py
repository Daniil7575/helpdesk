from django.urls import path, include
from .views import UserRegisterAPIView, ChangePasswordAPIView
from django_rest_passwordreset import urls

urlpatterns = [
    # path('', RegisterAPIView.as_view()),
    path('register/', UserRegisterAPIView.as_view(), name='register'),
    path('change-password/', ChangePasswordAPIView.as_view(),
         name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls'))
]
