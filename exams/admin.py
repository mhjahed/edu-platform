from django.contrib import admin
from .models import Exam, Question, ExamRegistration, ExamAttempt, Answer


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ['question_text', 'question_type', 'points', 'order']
    ordering = ['order']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['exam_code', 'title', 'examiner', 'status', 'exam_start', 'registered_count', 'created_at']
    list_filter = ['status', 'exam_start', 'created_at', 'examiner']
    search_fields = ['exam_code', 'title', 'examiner__username']
    date_hierarchy = 'exam_start'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('exam_code', 'title', 'description', 'examiner')
        }),
        ('Timing', {
            'fields': ('duration_minutes', 'registration_start', 'registration_end', 'exam_start', 'exam_end')
        }),
        ('Settings', {
            'fields': ('max_participants', 'passing_score', 'show_results_immediately', 'allow_review', 'status')
        }),
    )
    
    inlines = [QuestionInline]
    
    def registered_count(self, obj):
        return obj.registered_count
    registered_count.short_description = 'Registered'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'order', 'question_type', 'points', 'created_at']
    list_filter = ['question_type', 'exam', 'created_at']
    search_fields = ['question_text', 'exam__title', 'exam__exam_code']
    ordering = ['exam', 'order']


@admin.register(ExamRegistration)
class ExamRegistrationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'exam', 'status', 'registered_at', 'verification_date']
    list_filter = ['status', 'registered_at', 'exam']
    search_fields = ['candidate__username', 'full_name', 'email', 'exam__exam_code']
    date_hierarchy = 'registered_at'
    ordering = ['-registered_at']
    
    fieldsets = (
        ('Registration Details', {
            'fields': ('exam', 'candidate', 'status')
        }),
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number', 'student_id', 'institution')
        }),
        ('Verification', {
            'fields': ('verified_by', 'verification_date', 'rejection_reason'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['verify_registrations', 'reject_registrations']
    
    def verify_registrations(self, request, queryset):
        queryset.update(status='verified', verified_by=request.user)
        self.message_user(request, f"{queryset.count()} registrations verified.")
    verify_registrations.short_description = "Verify selected registrations"
    
    def reject_registrations(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} registrations rejected.")
    reject_registrations.short_description = "Reject selected registrations"


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ['registration', 'start_time', 'end_time', 'submitted', 'score']
    list_filter = ['submitted', 'start_time', 'registration__exam']
    search_fields = ['registration__candidate__username', 'registration__exam__exam_code']
    date_hierarchy = 'start_time'
    ordering = ['-start_time']
    readonly_fields = ['duration_taken']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'points_earned', 'created_at']
    list_filter = ['is_correct', 'question__question_type', 'created_at']
    search_fields = ['attempt__registration__candidate__username', 'question__question_text']
    ordering = ['-created_at']
