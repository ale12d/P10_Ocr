from rest_framework.serializers import ModelSerializer
 
from issue_tracking.models import Projects, Issues, Comments, Users
 
class ProjectsSerializer(ModelSerializer):
 
    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'author_user_id']

class IssuesSerializer(ModelSerializer):
 
    class Meta:
        model = Issues
        fields = ['title', 'desc', 'tag', 'priority', 'project_id', 'status', 'author_user_id', 'assignee_user_id', 'created_time']

class CommentsSerializer(ModelSerializer):
 
    class Meta:
        model = Comments
        fields = ['description', 'author_user_id', 'issue_id', 'created_time']


class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password']