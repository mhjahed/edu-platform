from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
)
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from .models import Exam, Question, ExamRegistration, ExamAttempt, Answer
from .forms import ExamCreateForm, QuestionForm, ExamRegistrationForm


# Examiner Views
class ExaminerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'exams/examiner_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_examiner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get examiner's exams
        exams = Exam.objects.filter(examiner=user).order_by('-created_at')
        
        # Calculate statistics
        context.update({
            'exams': exams[:10],  # Show last 10 exams
            'total_exams': exams.count(),
            'active_exams': exams.filter(status__in=['published', 'ongoing']).count(),
            'total_registrations': ExamRegistration.objects.filter(
                exam__examiner=user, status='verified'
            ).count(),
            'pending_verifications': ExamRegistration.objects.filter(
                exam__examiner=user, status='pending'
            ).count(),
            'upcoming_exams': exams.filter(
                exam_start__gt=timezone.now(), 
                status__in=['published', 'ongoing']
            ).order_by('exam_start')[:5],
        })
        
        # Add recent activities (placeholder data for now)
        context['recent_activities'] = [
            {
                'title': 'New registration',
                'description': 'Student registered for exam',
                'icon': 'user-plus',
                'type': 'success',
                'created_at': timezone.now()
            }
        ]
        
        return context


class CreateExamView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamCreateForm
    template_name = 'exams/create_exam.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_examiner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.examiner = self.request.user
        
        # Handle different action types
        action = self.request.POST.get('action', 'save_draft')
        if action == 'save_draft':
            form.instance.status = 'draft'
        
        response = super().form_valid(form)
        
        if action == 'save_continue':
            messages.success(self.request, 'Exam created successfully! Now add questions.')
            return redirect('exams:manage_questions', pk=self.object.pk)
        else:
            messages.success(self.request, 'Exam saved as draft successfully!')
            return redirect('exams:examiner_dashboard')
    
    def get_success_url(self):
        return reverse_lazy('exams:examiner_dashboard')


class EditExamView(LoginRequiredMixin, UpdateView):
    model = Exam
    fields = ['title', 'description', 'duration_minutes', 'registration_start', 'registration_end', 'exam_start', 'exam_end']
    template_name = 'exams/edit_exam.html'
    success_url = reverse_lazy('exams:examiner_dashboard')


class DeleteExamView(LoginRequiredMixin, DeleteView):
    model = Exam
    template_name = 'exams/delete_exam.html'
    success_url = reverse_lazy('exams:examiner_dashboard')


class ManageQuestionsView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/manage_questions.html'
    context_object_name = 'exam'


class AddQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['question_text', 'question_type', 'points', 'order', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
    template_name = 'exams/add_question.html'
    
    def form_valid(self, form):
        exam = get_object_or_404(Exam, pk=self.kwargs['pk'])
        form.instance.exam = exam
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('exams:manage_questions', kwargs={'pk': self.kwargs['pk']})


class EditQuestionView(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['question_text', 'question_type', 'points', 'order', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer']
    template_name = 'exams/edit_question.html'
    
    def get_success_url(self):
        return reverse_lazy('exams:manage_questions', kwargs={'pk': self.object.exam.pk})


class DeleteQuestionView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'exams/delete_question.html'
    
    def get_success_url(self):
        return reverse_lazy('exams:manage_questions', kwargs={'pk': self.object.exam.pk})


class ExamRegistrationsView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/exam_registrations.html'
    context_object_name = 'exam'


class VerifyRegistrationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        registration = get_object_or_404(ExamRegistration, pk=pk)
        registration.status = 'verified'
        registration.verified_by = request.user
        registration.save()
        messages.success(request, 'Registration verified successfully.')
        return redirect('exams:exam_registrations', pk=registration.exam.pk)


class RejectRegistrationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        registration = get_object_or_404(ExamRegistration, pk=pk)
        registration.status = 'rejected'
        registration.save()
        messages.success(request, 'Registration rejected.')
        return redirect('exams:exam_registrations', pk=registration.exam.pk)


class ExamResultsView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/exam_results.html'
    context_object_name = 'exam'


class ExportResultsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Placeholder for PDF export functionality
        return HttpResponse('PDF export functionality will be implemented here')


class PublishExamView(LoginRequiredMixin, View):
    def post(self, request, pk):
        exam = get_object_or_404(Exam, pk=pk)
        exam.status = 'published'
        exam.save()
        messages.success(request, 'Exam published successfully.')
        return redirect('exams:examiner_dashboard')


# Candidate Views
class ExamListView(ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'
    paginate_by = 10
    
    def get_queryset(self):
        return Exam.objects.filter(status='published')


class ExamDetailView(DetailView):
    model = Exam
    template_name = 'exams/exam_detail.html'
    context_object_name = 'exam'


class ExamRegistrationView(LoginRequiredMixin, CreateView):
    model = ExamRegistration
    fields = ['full_name', 'email', 'phone_number', 'student_id', 'institution']
    template_name = 'exams/exam_registration.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_candidate:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        exam = get_object_or_404(Exam, pk=self.kwargs['pk'])
        form.instance.exam = exam
        form.instance.candidate = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('exams:my_registrations')


class RegistrationPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Placeholder for PDF generation
        return HttpResponse('PDF generation will be implemented here')


class MyRegistrationsView(LoginRequiredMixin, ListView):
    model = ExamRegistration
    template_name = 'exams/my_registrations.html'
    context_object_name = 'registrations'
    
    def get_queryset(self):
        return ExamRegistration.objects.filter(candidate=self.request.user)


class ExamInstructionsView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/exam_instructions.html'
    context_object_name = 'exam'


class StartExamView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Logic to start exam
        return redirect('exams:take_exam', pk=pk)


class TakeExamView(LoginRequiredMixin, TemplateView):
    template_name = 'exams/take_exam.html'


class AutoSaveAnswersView(LoginRequiredMixin, View):
    def post(self, request, pk):
        return JsonResponse({'status': 'success'})


class SubmitExamView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Logic to submit exam
        messages.success(request, 'Exam submitted successfully!')
        return redirect('exams:exam_result', pk=pk)


class ExamResultView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/exam_result.html'
    context_object_name = 'exam'


class ResultPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # Placeholder for result PDF
        return HttpResponse('Result PDF will be implemented here')
