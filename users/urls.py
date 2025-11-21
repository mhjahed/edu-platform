from django.urls import path
from . import views

urlpatterns = [
    # Examiner authentication
    path('examiner/signup/', views.examiner_signup, name='examiner_signup'),
    path('examiner/login/', views.examiner_login, name='examiner_login'),
    path('examiner/profile/', views.examiner_profile, name='examiner_profile'),
    
    # Candidate authentication
    path('candidate/signup/', views.candidate_signup, name='candidate_signup'),
    path('candidate/login/', views.candidate_login, name='candidate_login'),
    path('candidate/profile/', views.candidate_profile, name='candidate_profile'),
    
    # Common
    path('logout/', views.logout_view, name='logout'),
]