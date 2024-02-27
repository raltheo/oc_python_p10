from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("project", views.ProjectView.as_view()),
    path("project/<int:project_id>", views.ProjectDetailView.as_view()),
    path("issue", views.IssueView.as_view()),
    path("issue/<int:issue_id>", views.IssueDetailView.as_view()),
    path("comment", views.CommentView.as_view()),
    path("comment/manage/<int:comment_id>", views.CommentDetailView.as_view()),
]
