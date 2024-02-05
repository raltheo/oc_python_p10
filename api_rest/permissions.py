from rest_framework.permissions import BasePermission
from .models import Contributor, Issue

class IsContributorPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return self.has_permission_post(request, view)
        elif request.method == 'GET':
            return self.has_permission_get(request, view)
        else:
            return False

    def has_permission_post(self, request, view):
        if request.data.get('project_id') and not request.data.get('issue_id'):
            project_id = request.data.get('project_id')
        else:
            issue = Issue.objects.get(id=request.data.get('issue_id'))
            project_id = issue.project_id
        return self.check_contributor(request.user, project_id)

    def has_permission_get(self, request, view):
        if view.kwargs.get('project_id') and not view.kwargs.get('issue_id'):
            project_id = view.kwargs.get('project_id')
        else:
            issue = Issue.objects.get(id=view.kwargs.get('issue_id'))
            project_id = issue.project_id
        return self.check_contributor(request.user, project_id)

    def check_contributor(self, user, project_id):
        if not project_id:
            return False

        try:
            contributor = Contributor.objects.get(user=user, projects__id=project_id)
            return True
        except Contributor.DoesNotExist:
            return False
        

