# accounts/urls.py
from django.urls import path, include
from .views import mypage

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path('join/', include("dj_rest_auth.registration.urls")),
    path('mypage/', mypage),
]
