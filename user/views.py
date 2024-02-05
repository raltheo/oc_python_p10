from functools import partial
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import MyUser
from api_rest.models import Contributor, Project

# Create your views here.
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
        

class ContributorView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):

        try:
            contributor = get_object_or_404(Contributor, user=request.user)
            project = get_object_or_404(Project, id=project_id)
            if project not in contributor.projects.all():
                contributor.projects.add(project)
            return Response({'message': 'You are now contributor of this project !'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, project_id):
        try:
            contributor = get_object_or_404(Contributor, user=request.user)
            project = get_object_or_404(Project, id=project_id)

            if project.creator == request.user or project in contributor.projects.all():
                contributor.projects.remove(project)
                return Response({'message': 'Remove successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'You do this.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)