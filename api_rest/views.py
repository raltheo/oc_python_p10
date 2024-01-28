from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Issue, MyUser, Project
from .serializers import ProjectSerializer, IssueSerializer, ProjectDetailSerializer
from django.shortcuts import get_object_or_404
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
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProjectView(APIView):
    # permission_classes = [IsAuthenticated]

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
            project.contributors.set([request.user])
            return Response({'message': 'Project created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProjectDetailView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class IssueView(APIView):
    # permission_classes = [IsAuthenticated]

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
                assigned_to=request.user,
                project=project
            )
            
            return Response({'message': 'Issue created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        issues = Issue.objects.all()
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)