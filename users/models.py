from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[('Examiner', 'Examiner'), ('Candidate', 'Candidate')],
        default='Candidate'
    )
    
    # Common fields
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Examiner specific fields
    position = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    
    # Candidate specific fields
    school = models.CharField(max_length=200, blank=True)
    class_grade = models.CharField(max_length=50, blank=True)
    group = models.CharField(
        max_length=20,
        choices=[
            ('Science', 'Science'),
            ('Arts', 'Arts'),
            ('Commerce', 'Commerce'),
            ('N/A', 'N/A')
        ],
        default='N/A'
    )
    whatsapp = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
