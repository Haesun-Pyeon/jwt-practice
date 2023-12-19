# accounts/urls.py
from django.urls import path, include
from .views import (
    UserCreateView,
    UserDetailView,
)

urlpatterns = [
    path("", include("dj_rest_auth.urls")), # 이거 한줄이면 로그인, 로그아웃, 토큰재발급, 비밀번호변경 다 있음
    #회원가입, 유저정보는 dj_rest_auth 그대로 쓰기보다는 추가항목들도 있으니 view 만드는걸 추천
    path('signup/', UserCreateView.as_view(), name='signup'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'), 
]