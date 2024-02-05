from django.db import models
from user.models import MyUser
import uuid

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    project_type = models.CharField(max_length=20, choices=[('backend', 'Back-end'), ('frontend', 'Front-end'), ('ios', 'iOS'), ('android', 'Android')])
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='project_author')
    created_time = models.DateTimeField(auto_now_add=True)


class Contributor(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    projects = models.ManyToManyField(Project)
    created_time = models.DateTimeField(auto_now_add=True)

class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='assigned_issues')
    priority = models.CharField(max_length=10, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')])
    tag = models.CharField(max_length=10, choices=[('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')])
    status = models.CharField(max_length=20, choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Finished', 'Finished')], default='To Do')
    created_time = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    content = models.TextField()
    unique_identifier = models.UUIDField(default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
