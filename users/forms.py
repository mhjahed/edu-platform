from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ExaminerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    position = forms.CharField(max_length=100, required=True)
    profession = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'position', 'profession', 'address', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create profile
            profile = Profile.objects.create(
                user=user,
                role='Examiner',
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
                position=self.cleaned_data['position'],
                profession=self.cleaned_data['profession'],
                address=self.cleaned_data['address']
            )
        return user

class CandidateSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    school = forms.CharField(max_length=200, required=True)
    class_grade = forms.CharField(max_length=50, required=True)
    group = forms.ChoiceField(choices=[
        ('Science', 'Science'),
        ('Arts', 'Arts'),
        ('Commerce', 'Commerce'),
        ('N/A', 'N/A')
    ], required=True)
    whatsapp = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'school', 'class_grade', 'group', 'whatsapp', 'address', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create profile
            profile = Profile.objects.create(
                user=user,
                role='Candidate',
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data['email'],
                school=self.cleaned_data['school'],
                class_grade=self.cleaned_data['class_grade'],
                group=self.cleaned_data['group'],
                whatsapp=self.cleaned_data['whatsapp'],
                address=self.cleaned_data['address']
            )
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'email', 'address', 'position', 'profession', 'school', 'class_grade', 'group', 'whatsapp']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide fields based on role
        if self.instance.role == 'Examiner':
            self.fields['school'].widget = forms.HiddenInput()
            self.fields['class_grade'].widget = forms.HiddenInput()
            self.fields['group'].widget = forms.HiddenInput()
            self.fields['whatsapp'].widget = forms.HiddenInput()
        else:
            self.fields['position'].widget = forms.HiddenInput()
            self.fields['profession'].widget = forms.HiddenInput()