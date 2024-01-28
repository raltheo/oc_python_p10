from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("register", views.UserRegistrationView.as_view()),
    path("token", TokenObtainPairView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
    path("project", views.ProjectView.as_view()),
    path("project/<int:project_id>", views.ProjectDetailView.as_view()),
    path('issue', views.IssueView.as_view()),
]