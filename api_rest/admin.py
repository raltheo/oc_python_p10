from django.contrib import admin
from .models import Comment, Project, Contributor, Issue

# Register your models here.
admin.site.register(Comment)
admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
