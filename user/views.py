from functools import partial
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import MyUser
from .serializers import MyUserSerializer
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
            if int(data["age"]) < 15:
                return Response({'error': 'Your too young !'}, status=status.HTTP_401_UNAUTHORIZED)
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
            return Response({'error': str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)
        

class UserView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def delete(self, request):
        user = get_object_or_404(MyUser, id=request.user.id)
        try:
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)

    def get(self, request):
        user = get_object_or_404(MyUser, id=request.user.id)
        serializer = MyUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request):
        user = get_object_or_404(MyUser, pk=request.user.id)
        
        serializer = MyUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({'error': str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)
        
    def delete(self, request, project_id):
        try:
            contributor = get_object_or_404(Contributor, user=request.user)
            project = get_object_or_404(Project, id=project_id)
            if project in contributor.projects.all():
                contributor.projects.remove(project)
                return Response({'message': 'You are no longer a contributor of this project.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'You are not a contributor of this project.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)