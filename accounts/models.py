from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    USER_ROLES = (
        ('examiner', 'Examiner'),
        ('candidate', 'Candidate'),
    )
    
    role = models.CharField(max_length=20, choices=USER_ROLES, null=False, blank=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Additional fields for candidates
    student_id = models.CharField(max_length=20, blank=True, null=True)
    institution = models.CharField(max_length=100, blank=True)
    
    # Additional fields for examiners
    department = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_examiner(self):
        return self.role == 'examiner'
    
    @property
    def is_candidate(self):
        return self.role == 'candidate'
