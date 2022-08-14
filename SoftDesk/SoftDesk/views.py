from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from SoftDesk.serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer, UsersSerializer, ContributorsSerializer
from django.contrib.auth import authenticate
from django.urls import reverse
from issue_tracking.models import Contributor, Project, Issue, Comment, User
import requests, json
from rest_framework.permissions import AllowAny
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from .permission import is_Contributor, is_Author
import jwt
from rest_framework import generics
from django.contrib.auth.signals import user_logged_in
from rest_framework_simplejwt.tokens import AccessToken

class ProjectsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = []
        contributors = get_list_or_404(Contributor, user_id=request.user)
        for i in range(len(contributors)):
            projects = projects + get_list_or_404(Project, id=contributors[i].project_id.id)
        serializer = ProjectsSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['author_user_id'] = request.user.id
        serializer = ProjectsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            project = get_object_or_404(Project, id=serializer.data['id'])
            contributor = Contributor(user_id=request.user,project_id=project, permission = 'author',role = 'admin')
            contributor.save()

            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProjectsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, is_Contributor, is_Author]
    def get(self, request, project_id):
        self.check_object_permissions(request, project_id)
        project = get_object_or_404(Project, id=project_id)
        serializer = ProjectsSerializer(project)
        return Response(serializer.data)

    def delete(self, request, project_id):
        item = get_object_or_404(Project, id=project_id)
        self.check_object_permissions(request, item)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, project_id):
        item = Project.objects.get(id=project_id)
        serializer = ProjectsSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})


class IssuesAPIView(APIView):
    permission_classes = [IsAuthenticated, is_Contributor]

    def get(self, request, project_id):
        self.check_object_permissions(request, project_id)
        issues = get_list_or_404(Issue, project_id=project_id)
        serializer = IssuesSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        self.check_object_permissions(request, project_id)
        request.data['project_id'] = project_id
        request.data['author_user_id'] = request.user.id
        serializer = IssuesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class IssuesDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, is_Contributor, is_Author]

    def delete(self, request, project_id, issue_id):
        issue = get_object_or_404(Issue, author_user_id=request.user, project_id=project_id, id=issue_id)
        self.check_object_permissions(request, issue)
        issue.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, project_id, issue_id):
        issue = get_object_or_404(Issue, author_user_id=request.user, project_id=project_id, id=issue_id)
        self.check_object_permissions(request, issue)
        serializer = IssuesSerializer(issue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})


class CommentsAPIView(APIView):
    permission_classes = [IsAuthenticated, is_Contributor]

    def get(self, request, project_id, issue_id):
        self.check_object_permissions(request, project_id)
        comments = get_list_or_404(Comment, issue_id=issue_id)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, project_id, issue_id):
        self.check_object_permissions(request, project_id)
        request.data['issue_id'] = issue_id
        request.data['author_user_id'] = request.user.id
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CommentsDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, is_Contributor, is_Author]

    def get(self, request, project_id, issue_id, comment_id):
        self.check_object_permissions(request, project_id)
        comment = get_object_or_404(Comment, issue_id=issue_id, id=comment_id)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data)

    def patch(self, request, project_id, issue_id, comment_id):
        comment = get_object_or_404(Comment, author_user_id=request.user, issue_id=issue_id, id=comment_id)
        self.check_object_permissions(request, comment)
        serializer = CommentsSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})

    def delete(self, request, project_id, issue_id, comment_id):
        item = get_object_or_404(Comment, author_user_id=request.user, issue_id=issue_id, id=comment_id)
        self.check_object_permissions(request, item)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)


class UsersAPIView(APIView):
    permission_classes = [IsAuthenticated, is_Contributor]

    def get(self, request, project_id):
        self.check_object_permissions(request, project_id)
        contributors = get_list_or_404(Contributor, project_id=project_id)
        serializer = ContributorsSerializer(contributors, many=True)
        return Response(serializer.data)

    def post(self, request, project_id):
        self.check_object_permissions(request, project_id)
        request.data['project_id'] = project_id
        serializer = ContributorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UsersDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, is_Contributor, is_Author]

    def delete(self, request, project_id, user_id):
        item = get_object_or_404(Contributor, project_id=project_id, user_id=user_id)
        self.check_object_permissions(request, item)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_204_NO_CONTENT)


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        try:
            obj =  UsersSerializer(data=request.data)
            if obj.is_valid():
                user = User.objects.create_user(obj['email'].value, obj['first_name'].value, obj['last_name'].value, obj['password'].value)
                return Response({'Message': 'valid sign up'}, status=status.HTTP_200_OK)
            return Response(obj.errors,status = status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'Message':'Something Failed due to {}'.format(str(e))}, status = status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        try:
            input_data = request.data
            email = input_data.get('email')
            password = input_data.get('password')

            user = authenticate(email=email, password=password)
            if user is not None:
                try:
                    token = AccessToken.for_user(user)
                    user_details = {}
                    user_details['name'] = "%s %s" % (
                        user.first_name, user.last_name)
                    user_details['token'] = str(token)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
                res = {'error': 'please provide a email and a password'}
                return Response(res)
