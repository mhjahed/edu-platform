from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    subject = models.CharField(max_length=200)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_inquiries')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_inquiries', null=True, blank=True)
    
    # If inquiry is related to a specific exam
    exam = models.ForeignKey('exams.Exam', on_delete=models.CASCADE, null=True, blank=True, related_name='inquiries')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.sender.username}"
    
    @property
    def latest_message(self):
        return self.messages.first()
    
    @property
    def message_count(self):
        return self.messages.count()


class InquiryMessage(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(upload_to='inquiry_attachments/', blank=True, null=True)
    
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.inquiry.subject} - {self.sender.username} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
