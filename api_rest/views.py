from functools import partial
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Issue, MyUser, Project, Comment, Contributor
from .serializers import ProjectSerializer, IssueSerializer, ProjectDetailSerializer, IssueDetailSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsContributorPermission
# Create your views here.

# https://openclassrooms.com/fr/courses/7192416-mettez-en-place-une-api-avec-django-rest-framework/7424720-donnez-des-acces-avec-les-tokens

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        required_fields = ['username', 'password', 'age', 'can_be_contacted', 'can_data_be_shared']
        if not all(field in data for field in required_fields):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = MyUser.objects.create_user(
                username=data['username'],
                password=data['password'],
                age=data['age'],
                can_be_contacted=data['can_be_contacted'],
                can_data_be_shared=data['can_data_be_shared']
            )
            Contributor.objects.create(user=user)
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
 
class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        data = request.data

        required_fields = ['name', 'description', 'type']
        if not all(field in data for field in required_fields):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.create(
                name=data['name'],
                description=data['description'],
                project_type=data['type'],
                author=request.user
            )
            contributor = Contributor.objects.get(user=request.user)
            contributor.projects.set([project])
            return Response({'message': 'Project created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProjectDetailView(APIView):

    permission_classes = [IsAuthenticated, IsContributorPermission]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)

        if project.author == request.user:
            project.delete()
            return Response({'message': 'Project deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You are not the author of this project'}, status=status.HTTP_403_FORBIDDEN)

class IssueView(APIView):
    permission_classes = [IsAuthenticated, IsContributorPermission]
    
    def post(self, request):
        data = request.data

        required_fields = ['name', 'description', 'priority', 'tag', 'status', 'project_id']
        if not all(field in data for field in required_fields):

            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        project = get_object_or_404(Project, pk=data["project_id"])
        
        try:
            issue = Issue.objects.create(
                name=data['name'],
                description=data['description'],
                priority=data['priority'],
                tag=data['tag'],
                status=data['status'],
                author=request.user,
                project=project
            )
            
            return Response({'message': 'Issue created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class IssueDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)

        if issue.author == request.user:
            issue.delete()
            return Response({'message': 'Issue deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You are not the author of this issue'}, status=status.HTTP_403_FORBIDDEN)
    

class IssueDetailView(APIView):

    permission_classes = [IsAuthenticated, IsContributorPermission]

    def get(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)
        serializer = IssueDetailSerializer(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class IssuetUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, issue_id):
        issue = get_object_or_404(Issue, pk=issue_id)

        if issue.author == request.user:
            serializer = IssueSerializer(issue, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Issue updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'You are not the author of this issue'}, status=status.HTTP_403_FORBIDDEN)


class CommentView(APIView):
    permission_classes = [IsAuthenticated, IsContributorPermission]

    def post(self, request):
        data = request.data

        required_fields = ['issue_id', 'content']
        if not all(field in data for field in required_fields):
 
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        issue = get_object_or_404(Issue, pk=data["issue_id"])
        
        try:
            comment = Comment.objects.create(
                content=data['content'],
                author=request.user,
                issue=issue
            )
            
            return Response({'message': 'Comment created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    

class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        
        if comment.author == request.user:
            comment.delete()
            return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You are not the author of this comment'}, status=status.HTTP_403_FORBIDDEN)
        

class CommentUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.author == request.user:
            serializer = IssueSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Comment updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'You are not the author of this comment'}, status=status.HTTP_403_FORBIDDEN)