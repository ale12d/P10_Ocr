from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from issue_tracking.models import Project, Issue, Comment, User, Contributor


class ProjectsSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']


class IssuesSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project_id', 'status', 'author_user_id', 'assignee_user_id', 'created_time']


class CommentsSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']


class UsersSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']


class ContributorsSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user_id', 'project_id', 'permission', 'role']
