from django.contrib import admin
from .models import Profile,User,Project,Assignment,Task

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Assignment)
admin.site.register(Task)

