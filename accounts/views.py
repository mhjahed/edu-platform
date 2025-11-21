from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView as BasePasswordChangeView,
    PasswordResetView as BasePasswordResetView, PasswordResetDoneView as BasePasswordResetDoneView,
    PasswordResetConfirmView as BasePasswordResetConfirmView, 
    PasswordResetCompleteView as BasePasswordResetCompleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return reverse_lazy('home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'You have been successfully logged out.')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(TemplateView):
    template_name = 'accounts/register.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Forms are now defined in forms.py


class ExaminerRegisterView(CreateView):
    model = User
    form_class = None  # Will be set in get_form_class
    template_name = 'accounts/examiner_register.html'
    success_url = reverse_lazy('accounts:login')
    
    def get_form_class(self):
        from .forms import ExaminerRegistrationForm
        return ExaminerRegistrationForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Examiner account created successfully! Please log in.')
        return response


class CandidateRegisterView(CreateView):
    model = User
    form_class = None  # Will be set in get_form_class
    template_name = 'accounts/candidate_register.html'
    success_url = reverse_lazy('accounts:login')
    
    def get_form_class(self):
        from .forms import CandidateRegistrationForm
        return CandidateRegistrationForm
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Candidate account created successfully! Please log in.')
        return response


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = None  # Will be set in get_form_class
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_form_class(self):
        from .forms import ProfileUpdateForm
        return ProfileUpdateForm
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


# Password management views
class PasswordChangeView(BasePasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully!')
        return super().form_valid(form)


class PasswordResetView(BasePasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'


class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetCompleteView(BasePasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
