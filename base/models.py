from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_candidate = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)  # Example additional field
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Example additional field
    token = models.CharField(max_length=32, blank=True, null=True)  

    def __str__(self):
        return f'{self.user.username} Profile'

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_tasks = models.IntegerField(default=0)  # Total tasks in the project
    completed_tasks = models.IntegerField(default=0)  # Completed tasks
    remaining_tasks = models.IntegerField(default=0)  # Remaining tasks

    def __str__(self):
        return self.title
    
class Assignment(models.Model):
    project = models.ForeignKey(Project, related_name='assignments', on_delete=models.CASCADE)  # Add related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    completed_tasks = models.IntegerField(default=0)
    score = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        project = self.project
        total_tasks = project.total_tasks
        self.score = (self.completed_tasks / total_tasks) * 100 if total_tasks else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.project.title}"


    
    
class Task(models.Model):
            STATUS_CHOICES = [
                ('not_started', 'Not Started'),
                ('in_progress', 'In Progress'),
                ('completed', 'Completed'),
            ]

            project = models.ForeignKey(Project, related_name="tasks", on_delete=models.CASCADE)
            title = models.CharField(max_length=255)
            description = models.TextField()
            status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
            assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # Candidate assigned to this task
            def __str__(self):
                return self.title