from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ExaminerSignUpForm, CandidateSignUpForm, ProfileUpdateForm

def examiner_signup(request):
    if request.method == 'POST':
        form = ExaminerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Examiner account created successfully!')
            return redirect('examiner_dashboard')
    else:
        form = ExaminerSignUpForm()
    return render(request, 'users/examiner_signup.html', {'form': form})

def candidate_signup(request):
    if request.method == 'POST':
        form = CandidateSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Candidate account created successfully!')
            return redirect('candidate_home')
    else:
        form = CandidateSignUpForm()
    return render(request, 'users/candidate_signup.html', {'form': form})

def examiner_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, 'profile') and user.profile.role == 'Examiner':
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('examiner_dashboard')
            else:
                messages.error(request, 'This account is not authorized for examiner access.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/examiner_login.html', {'form': form})

def candidate_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, 'profile') and user.profile.role == 'Candidate':
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('candidate_home')
            else:
                messages.error(request, 'This account is not authorized for candidate access.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/candidate_login.html', {'form': form})

@login_required
def examiner_profile(request):
    if request.user.profile.role != 'Examiner':
        return redirect('home')
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('examiner_profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'users/examiner_profile.html', {'form': form})

@login_required
def candidate_profile(request):
    if request.user.profile.role != 'Candidate':
        return redirect('home')
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('candidate_profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'users/candidate_profile.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')
