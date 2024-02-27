from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register", views.UserRegistrationView.as_view()),
    path("token", TokenObtainPairView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
    path("contributor/manage/<int:project_id>", views.ContributorView.as_view()),
    path("user", views.UserView.as_view()),
]
