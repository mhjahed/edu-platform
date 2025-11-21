from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

User = get_user_model()


class Exam(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    exam_code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    examiner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_exams')
    
    # Timing
    duration_minutes = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    exam_start = models.DateTimeField()
    exam_end = models.DateTimeField()
    
    # Settings
    max_participants = models.PositiveIntegerField(default=100)
    passing_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)
    show_results_immediately = models.BooleanField(default=False)
    allow_review = models.BooleanField(default=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.exam_code} - {self.title}"
    
    @property
    def is_registration_open(self):
        now = timezone.now()
        return self.registration_start <= now <= self.registration_end
    
    @property
    def is_exam_active(self):
        now = timezone.now()
        return self.exam_start <= now <= self.exam_end
    
    @property
    def total_questions(self):
        return self.questions.count()
    
    @property
    def registered_count(self):
        return self.registrations.filter(status='verified').count()


class Question(models.Model):
    QUESTION_TYPES = (
        ('mcq', 'Multiple Choice Question'),
        ('short_answer', 'Short Answer'),
        ('drag_drop', 'Drag and Drop'),
        ('true_false', 'True/False'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    points = models.FloatField(validators=[MinValueValidator(0.1)], default=1.0)
    order = models.PositiveIntegerField(default=1)
    
    # For MCQ and True/False
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_answer = models.CharField(max_length=500)  # Store correct answer key or text
    
    # For drag and drop or complex questions
    additional_data = models.JSONField(blank=True, null=True)  # Store drag-drop items, etc.
    
    explanation = models.TextField(blank=True)  # Optional explanation for the answer
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['exam', 'order']
    
    def __str__(self):
        return f"{self.exam.exam_code} - Q{self.order}"


class ExamRegistration(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='registrations')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Registration details that can be auto-filled from profile
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17)
    student_id = models.CharField(max_length=20, blank=True)
    institution = models.CharField(max_length=100, blank=True)
    
    # Verification
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_registrations')
    verification_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['exam', 'candidate']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.candidate.username} - {self.exam.exam_code}"


class ExamAttempt(models.Model):
    registration = models.OneToOneField(ExamRegistration, on_delete=models.CASCADE, related_name='attempt')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    submitted = models.BooleanField(default=False)
    score = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.registration.candidate.username} - {self.registration.exam.exam_code} Attempt"
    
    @property
    def time_remaining(self):
        if self.submitted or self.end_time:
            return 0
        
        exam_duration = timezone.timedelta(minutes=self.registration.exam.duration_minutes)
        elapsed = timezone.now() - self.start_time
        remaining = exam_duration - elapsed
        
        return max(0, remaining.total_seconds())
    
    @property
    def duration_taken(self):
        if self.end_time:
            return self.end_time - self.start_time
        elif self.submitted:
            return timezone.now() - self.start_time
        return None


class Answer(models.Model):
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()  # Store the selected answer or text input
    is_correct = models.BooleanField(null=True, blank=True)  # Calculated after submission
    points_earned = models.FloatField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.registration.candidate.username} - Q{self.question.order}"
