from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_user, name='register_user'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('verify/<str:token>/', verify_email, name='verify_email'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:token>/', reset_password, name='reset_password'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('candidate_dashboard/', candidate_dashboard, name='candidate_dashboard'),
    path('add_project/', add_project, name='add_project'),
    path('update_project/<int:project_id>/', update_project, name='update_project'),
    path('assign_project/<int:project_id>/', assign_project, name='assign_project'),
    path('delete_project/<int:project_id>/', delete_project, name='delete_project'),
    path('get_candidates/<int:project_id>/', get_candidates, name="get_candidates"),
     path('candidate_dashboard/', candidate_dashboard, name='candidate_dashboard'),
    path('project_progress/<int:project_id>/', project_progress, name='project_progress'),
    path('add_task/<int:project_id>/', add_task, name="add_task"),
     path('profile/settings/',profile_settings, name='profile_settings'),
    path('mark-as-completed/<int:project_id>/', mark_project_completed, name='mark_project_completed'),
]
