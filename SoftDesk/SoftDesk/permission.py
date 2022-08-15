from rest_framework import permissions
from django.conf import settings
import jwt
from issue_tracking.models import Contributor
from rest_framework import exceptions
from django.shortcuts import get_object_or_404, get_list_or_404


class is_Contributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        method = request.method
        if method in ('GET', 'POST'):
            try:
                get_list_or_404(Contributor, user_id=request.user, project_id=obj)
                return True
            except:
                raise exceptions.PermissionDenied(detail="you are not a contributor to this project")
        else:
            return True


class is_Author(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        method = request.method
        if method in ('DELETE', 'PATCH', 'POST'):
            if obj.author_user_id == request.user:
                return True
            else:
                raise exceptions.PermissionDenied(detail="you are not the author")

        elif method in ('GET', 'POST'):
            return True
        else:
            return False