from django.db import models

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)

class Projects(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class Contributors(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    permission = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

class Issues(models.Model):
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="author_user")
    assignee_user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="assignee_user")
    created_time = models.DateTimeField(auto_now_add=True)
                        
class Comments(models.Model):
    description = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)