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
]
