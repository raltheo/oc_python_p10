from rest_framework.permissions import BasePermission
from api_rest.models import Contributor, Issue
from django.shortcuts import get_object_or_404

class IsContributorPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return self.has_permission_post(request, view)
        elif request.method == 'GET':
            return self.has_permission_get(request, view)
        elif request.method == 'PUT':
            return self.has_permission_get(request, view)
        elif request.method == 'DELETE':
            return self.has_permission_get(request, view)
        else:
            return False

    def has_permission_post(self, request, view):
        if request.data.get('project_id') and not request.data.get('issue_id'):
            project_id = request.data.get('project_id')
        else:
            issue = get_object_or_404(Issue, id=request.data.get('issue_id'))
            project_id = issue.project_id
        return self.check_contributor(request.user, project_id)

    def has_permission_get(self, request, view):
        if view.kwargs.get('project_id') and not view.kwargs.get('issue_id'):
            project_id = view.kwargs.get('project_id')
        else:
            issue = get_object_or_404(Issue, id=view.kwargs.get('issue_id'))
            project_id = issue.project_id
        return self.check_contributor(request.user, project_id)

    
    
    def check_contributor(self, user, project_id):
        if not project_id:
            return False

        try:
            get_object_or_404(Contributor, user=user, projects__id=project_id)
            return True
        except Contributor.DoesNotExist:
            return False
        

