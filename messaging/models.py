from django.db import models
from django.contrib.auth.models import User
from exams.models import Exam

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)  # Related exam
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    # Message types
    MESSAGE_TYPES = [
        ('inquiry', 'Inquiry'),
        ('request', 'Request'),
        ('notification', 'Notification'),
        ('reply', 'Reply'),
    ]
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='inquiry')

    def __str__(self):
        return f"{self.subject} - {self.sender.username} to {self.receiver.username}"

class Request(models.Model):
    """Student requests/inquiries system"""
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Request status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('replied', 'Replied'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Examiner reply
    reply = models.TextField(blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    replied_by = models.ForeignKey(User, related_name='replied_requests', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.subject} - {self.student.username}"
