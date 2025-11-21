from django.contrib.admin import AdminSite
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

class ExamManagementAdminSite(AdminSite):
    site_header = "🎓 Exam Management System"
    site_title = "Exam Management Admin"
    index_title = "Welcome to Exam Management System Administration"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
            path('system-stats/', self.admin_view(self.system_stats_view), name='system_stats'),
        ]
        return custom_urls + urls
    
    @staff_member_required
    def dashboard_view(self, request):
        from exams.models import Exam, Registration, Result
        from users.models import Profile
        from messaging.models import Request
        
        # Get current time
        now = timezone.now()
        
        # Calculate statistics
        total_exams = Exam.objects.count()
        active_exams = Exam.objects.filter(
            exam_start__lte=now,
            exam_end__gte=now
        ).count()
        
        upcoming_exams = Exam.objects.filter(
            exam_start__gt=now
        ).count()
        
        total_registrations = Registration.objects.count()
        pending_registrations = Registration.objects.filter(
            status='Pending Verification'
        ).count()
        
        total_students = Profile.objects.filter(role='Candidate').count()
        total_examiners = Profile.objects.filter(role='Examiner').count()
        
        total_results = Result.objects.count()
        pending_requests = Request.objects.filter(status='pending').count()
        
        # Recent activity
        recent_exams = Exam.objects.order_by('-created_at')[:5]
        recent_registrations = Registration.objects.order_by('-registration_date')[:5]
        recent_requests = Request.objects.order_by('-created_at')[:5]
        
        # Exam status breakdown
        exam_status = {
            'open_registration': Exam.objects.filter(registration_end__gt=now).count(),
            'in_progress': Exam.objects.filter(
                exam_start__lte=now,
                exam_end__gte=now
            ).count(),
            'completed': Exam.objects.filter(exam_end__lt=now).count(),
        }
        
        context = {
            'title': 'System Dashboard',
            'total_exams': total_exams,
            'active_exams': active_exams,
            'upcoming_exams': upcoming_exams,
            'total_registrations': total_registrations,
            'pending_registrations': pending_registrations,
            'total_students': total_students,
            'total_examiners': total_examiners,
            'total_results': total_results,
            'pending_requests': pending_requests,
            'recent_exams': recent_exams,
            'recent_registrations': recent_registrations,
            'recent_requests': recent_requests,
            'exam_status': exam_status,
            'now': now,
        }
        
        return render(request, 'admin/dashboard.html', context)
    
    @staff_member_required
    def system_stats_view(self, request):
        from exams.models import Exam, Registration, Result
        from users.models import Profile
        from messaging.models import Request
        
        # Detailed statistics
        stats = {
            'users': {
                'total': Profile.objects.count(),
                'examiners': Profile.objects.filter(role='Examiner').count(),
                'students': Profile.objects.filter(role='Candidate').count(),
                'active': Profile.objects.filter(user__is_active=True).count(),
            },
            'exams': {
                'total': Exam.objects.count(),
                'this_month': Exam.objects.filter(
                    created_at__gte=timezone.now().replace(day=1)
                ).count(),
                'by_type': list(Exam.objects.values('examiner_profession').annotate(
                    count=Count('id')
                )),
            },
            'registrations': {
                'total': Registration.objects.count(),
                'verified': Registration.objects.filter(status='Ready for Exam').count(),
                'pending': Registration.objects.filter(status='Pending Verification').count(),
                'invalid': Registration.objects.filter(status='Invalid').count(),
            },
            'results': {
                'total': Result.objects.count(),
                'passed': Result.objects.filter(score__gte=50).count(),
                'failed': Result.objects.filter(score__lt=50).count(),
                'average_score': Result.objects.aggregate(
                    avg_score=models.Avg('score')
                )['avg_score'] or 0,
            },
            'requests': {
                'total': Request.objects.count(),
                'pending': Request.objects.filter(status='pending').count(),
                'replied': Request.objects.filter(status='replied').count(),
                'resolved': Request.objects.filter(status='resolved').count(),
            }
        }
        
        context = {
            'title': 'System Statistics',
            'stats': stats,
        }
        
        return render(request, 'admin/system_stats.html', context)

# Create custom admin site instance
admin_site = ExamManagementAdminSite(name='exam_admin')

# Register all models with the custom admin site
from django.contrib.auth.models import User, Group
from users.models import Profile
from exams.models import Exam, Question, Registration, Result
from messaging.models import Message, Request

# Register models
admin_site.register(User)
admin_site.register(Group)
admin_site.register(Profile)
admin_site.register(Exam)
admin_site.register(Question)
admin_site.register(Registration)
admin_site.register(Result)
admin_site.register(Message)
admin_site.register(Request)
