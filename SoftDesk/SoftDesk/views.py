from rest_framework.views import APIView
from rest_framework.response import Response
 
from issue_tracking.models import Projects, Issues, Comments, Users
from SoftDesk.serializers import ProjectsSerializer, IssuesSerializer, CommentsSerializer, UsersSerializer
 
class ProjectsAPIView(APIView):
 
    def get(self, *args, **kwargs):
        projects = Projects.objects.all()
        serializer = ProjectsSerializer(projects, many=True)
        return Response(serializer.data)

class IssuesAPIView(APIView):
 
    def get(self, *args, **kwargs):
        issues = Issues.objects.all()
        serializer = IssuesSerializer(issues, many=True)
        return Response(serializer.data)

class CommentsAPIView(APIView):
 
    def get(self, *args, **kwargs):
        comments = Comments.objects.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data)

class UsersAPIView(APIView):

    def get(self, *args, **kwargs):
        user = Users.objects.all()
        serializer = UsersSerializer(user, many=True)
        return Response(serializer.data)