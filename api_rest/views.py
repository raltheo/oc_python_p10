from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Issue, Project, Comment, Contributor
from .serializers import (
    ProjectSerializer,
    IssueSerializer,
    ProjectDetailSerializer,
    IssueDetailSerializer,
    CommentSerializer,
)
from django.shortcuts import get_object_or_404
from user.permissions import IsContributorPermission
from rest_framework.pagination import PageNumberPagination

# Create your views here.

# https://openclassrooms.com/fr/courses/7192416-mettez-en-place-une-api-avec-django-rest-framework/7424720-donnez-des-acces-avec-les-tokens


class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        required_fields = ["name", "description", "type"]
        if not all(field in data for field in required_fields):
            return Response(
                {"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            project = Project.objects.create(
                name=data["name"],
                description=data["description"],
                project_type=data["type"],
                author=request.user,
            )
            contributor = Contributor.objects.get(user=request.user)
            contributor.projects.add(project)
            return Response(
                {"message": "Project created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_417_EXPECTATION_FAILED
            )

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10

        projects = Project.objects.all()
        result_page = paginator.paginate_queryset(projects, request)
        serializer = ProjectSerializer(result_page, many=True)
        # return paginator.get_paginated_response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, IsContributorPermission]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        if project.author == request.user:
            project.delete()
            return Response(
                {"message": "Project deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "You are not the author of this project"},
                status=status.HTTP_403_FORBIDDEN,
            )


class IssueView(APIView):
    permission_classes = [IsAuthenticated, IsContributorPermission]

    def post(self, request):
        data = request.data
        assigned_contributor = None
        required_fields = [
            "name",
            "description",
            "priority",
            "tag",
            "status",
            "project_id",
        ]
        if not all(field in data for field in required_fields):
            return Response(
                {"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST
            )
        project = get_object_or_404(Project, pk=data["project_id"])
        try:
            if "assigned_contributor" in data:
                assigned_contributor = get_object_or_404(
                    Contributor, pk=data["assigned_contributor"]
                )

                if project not in assigned_contributor.projects.all():
                    return Response(
                        {
                            "error": "The contributor you are trying to assign to this issue is not a contributor of the project."
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )

            issue = Issue.objects.create(
                name=data["name"],
                description=data["description"],
                priority=data["priority"],
                tag=data["tag"],
                status=data["status"],
                author=request.user,
                assigned_contributor=assigned_contributor,
                project=project,
            )

            return Response(
                {"message": "Issue created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_417_EXPECTATION_FAILED
            )


class IssueDetailView(APIView):
    permission_classes = [IsAuthenticated, IsContributorPermission]

    def delete(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)

        if issue.author == request.user:
            issue.delete()
            return Response(
                {"message": "Issue deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "You are not the author of this issue"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def get(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)
        serializer = IssueDetailSerializer(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)
        if issue.author == request.user:
            serializer = IssueSerializer(issue, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Issue updated successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "You are not the author of this issue"},
                status=status.HTTP_403_FORBIDDEN,
            )


class CommentView(APIView):
    permission_classes = [IsAuthenticated, IsContributorPermission]

    def post(self, request):
        data = request.data

        required_fields = ["issue_id", "content"]
        if not all(field in data for field in required_fields):
            return Response(
                {"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST
            )
        issue = get_object_or_404(Issue, pk=data["issue_id"])

        try:
            comment = Comment.objects.create(
                content=data["content"], author=request.user, issue=issue
            )

            return Response(
                {"message": "Comment created successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_417_EXPECTATION_FAILED
            )


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.author == request.user:
            comment.delete()
            return Response(
                {"message": "Comment deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "You are not the author of this comment"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.author == request.user:
            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Comment updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "You are not the author of this comment"},
                status=status.HTTP_403_FORBIDDEN,
            )
