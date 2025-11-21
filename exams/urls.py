from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    # Examiner URLs
    path('dashboard/', views.ExaminerDashboardView.as_view(), name='examiner_dashboard'),
    path('create/', views.CreateExamView.as_view(), name='create_exam'),
    path('<int:pk>/edit/', views.EditExamView.as_view(), name='edit_exam'),
    path('<int:pk>/delete/', views.DeleteExamView.as_view(), name='delete_exam'),
    path('<int:pk>/questions/', views.ManageQuestionsView.as_view(), name='manage_questions'),
    path('<int:pk>/questions/add/', views.AddQuestionView.as_view(), name='add_question'),
    path('question/<int:pk>/edit/', views.EditQuestionView.as_view(), name='edit_question'),
    path('question/<int:pk>/delete/', views.DeleteQuestionView.as_view(), name='delete_question'),
    path('<int:pk>/registrations/', views.ExamRegistrationsView.as_view(), name='exam_registrations'),
    path('registration/<int:pk>/verify/', views.VerifyRegistrationView.as_view(), name='verify_registration'),
    path('registration/<int:pk>/reject/', views.RejectRegistrationView.as_view(), name='reject_registration'),
    path('<int:pk>/results/', views.ExamResultsView.as_view(), name='exam_results'),
    path('<int:pk>/results/export/', views.ExportResultsView.as_view(), name='export_results'),
    path('<int:pk>/publish/', views.PublishExamView.as_view(), name='publish_exam'),
    
    # Candidate URLs
    path('', views.ExamListView.as_view(), name='exam_list'),
    path('<int:pk>/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('<int:pk>/register/', views.ExamRegistrationView.as_view(), name='exam_registration'),
    path('registration/<int:pk>/pdf/', views.RegistrationPDFView.as_view(), name='registration_pdf'),
    path('my-registrations/', views.MyRegistrationsView.as_view(), name='my_registrations'),
    path('<int:pk>/instructions/', views.ExamInstructionsView.as_view(), name='exam_instructions'),
    path('<int:pk>/start/', views.StartExamView.as_view(), name='start_exam'),
    path('<int:pk>/take/', views.TakeExamView.as_view(), name='take_exam'),
    path('attempt/<int:pk>/auto-save/', views.AutoSaveAnswersView.as_view(), name='auto_save_answers'),
    path('<int:pk>/submit/', views.SubmitExamView.as_view(), name='submit_exam'),
    path('<int:pk>/result/', views.ExamResultView.as_view(), name='exam_result'),
    path('result/<int:pk>/pdf/', views.ResultPDFView.as_view(), name='result_pdf'),
]