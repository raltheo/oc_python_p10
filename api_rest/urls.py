from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', views.getData),
    path("test", views.UserLoginView.as_view()),
    path("token", TokenObtainPairView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
]