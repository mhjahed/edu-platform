from django import forms
from django.forms import inlineformset_factory, formset_factory
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Exam, Question, ExamRegistration, Answer
from django.contrib.auth import get_user_model

User = get_user_model()


class ExamCreateForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'exam_code', 'title', 'description', 'duration_minutes',
            'registration_start', 'registration_end', 'exam_start', 'exam_end',
            'max_participants', 'passing_score', 'show_results_immediately', 'allow_review'
        ]
        widgets = {
            'exam_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., EXAM2025001'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter exam title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the exam content and instructions'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Duration in minutes'
            }),
            'registration_start': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'registration_end': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'exam_start': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'exam_end': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'value': 100
            }),
            'passing_score': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 100,
                'step': 0.1,
                'value': 50
            }),
            'show_results_immediately': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'allow_review': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        reg_start = cleaned_data.get('registration_start')
        reg_end = cleaned_data.get('registration_end')
        exam_start = cleaned_data.get('exam_start')
        exam_end = cleaned_data.get('exam_end')
        
        if reg_start and reg_end and reg_start >= reg_end:
            raise ValidationError('Registration end time must be after start time.')
        
        if exam_start and exam_end and exam_start >= exam_end:
            raise ValidationError('Exam end time must be after start time.')
        
        if reg_end and exam_start and reg_end > exam_start:
            raise ValidationError('Exam start time must be after registration end time.')
        
        return cleaned_data


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'question_text', 'question_type', 'points', 'order',
            'option_a', 'option_b', 'option_c', 'option_d',
            'correct_answer', 'explanation'
        ]
        widgets = {
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your question here'
            }),
            'question_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0.1,
                'step': 0.1,
                'value': 1.0
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'option_a': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option A'
            }),
            'option_b': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option B'
            }),
            'option_c': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option C'
            }),
            'option_d': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Option D'
            }),
            'correct_answer': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correct answer (A, B, C, D or text for short answer)'
            }),
            'explanation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Optional explanation for the correct answer'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question_type'].choices = Question.QUESTION_TYPES
    
    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get('question_type')
        
        if question_type in ['mcq', 'true_false']:
            # Validate that all options are provided for MCQ
            if question_type == 'mcq':
                required_options = ['option_a', 'option_b', 'option_c', 'option_d']
                for option in required_options:
                    if not cleaned_data.get(option):
                        raise ValidationError(f'All options (A, B, C, D) are required for multiple choice questions.')
        
        return cleaned_data


class ExamRegistrationForm(forms.ModelForm):
    class Meta:
        model = ExamRegistration
        fields = ['full_name', 'email', 'phone_number', 'student_id', 'institution']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your student ID'
            }),
            'institution': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your institution name'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Auto-fill from user profile if available
        if user and not self.instance.pk:
            self.fields['full_name'].initial = f"{user.first_name} {user.last_name}".strip()
            self.fields['email'].initial = user.email
            self.fields['phone_number'].initial = user.phone_number
            self.fields['student_id'].initial = user.student_id
            self.fields['institution'].initial = user.institution


class RegistrationVerificationForm(forms.ModelForm):
    class Meta:
        model = ExamRegistration
        fields = ['status', 'rejection_reason']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'rejection_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Provide reason for rejection (if applicable)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            ('verified', 'Verified'),
            ('rejected', 'Rejected'),
        ]


class ExamAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)
        
        for question in questions:
            field_name = f'question_{question.id}'
            
            if question.question_type == 'mcq':
                choices = []
                if question.option_a:
                    choices.append(('A', question.option_a))
                if question.option_b:
                    choices.append(('B', question.option_b))
                if question.option_c:
                    choices.append(('C', question.option_c))
                if question.option_d:
                    choices.append(('D', question.option_d))
                
                self.fields[field_name] = forms.ChoiceField(
                    choices=[('', 'Select an option')] + choices,
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=False,
                    label=question.question_text
                )
            
            elif question.question_type == 'true_false':
                self.fields[field_name] = forms.ChoiceField(
                    choices=[
                        ('', 'Select an option'),
                        ('True', 'True'),
                        ('False', 'False')
                    ],
                    widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                    required=False,
                    label=question.question_text
                )
            
            elif question.question_type == 'short_answer':
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea(attrs={
                        'class': 'form-control',
                        'rows': 4,
                        'placeholder': 'Enter your answer here'
                    }),
                    required=False,
                    label=question.question_text
                )
            
            elif question.question_type == 'drag_drop':
                # For now, treat as text input - can be enhanced later
                self.fields[field_name] = forms.CharField(
                    widget=forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Enter your answer'
                    }),
                    required=False,
                    label=question.question_text
                )


# Inline formset for questions
QuestionFormSet = inlineformset_factory(
    Exam, Question,
    form=QuestionForm,
    extra=1,
    can_delete=True,
    fields=[
        'question_text', 'question_type', 'points', 'order',
        'option_a', 'option_b', 'option_c', 'option_d',
        'correct_answer', 'explanation'
    ]
)