from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    # Inbox and messaging
    path('', views.InboxView.as_view(), name='inbox'),
    path('sent/', views.SentInquiriesView.as_view(), name='sent'),
    path('create/', views.CreateInquiryView.as_view(), name='create'),
    path('<int:pk>/', views.InquiryDetailView.as_view(), name='detail'),
    path('<int:pk>/reply/', views.ReplyToInquiryView.as_view(), name='reply'),
    path('<int:pk>/close/', views.CloseInquiryView.as_view(), name='close'),
    path('<int:pk>/delete/', views.DeleteInquiryView.as_view(), name='delete'),
    
    # AJAX endpoints
    path('mark-read/', views.MarkReadView.as_view(), name='mark_read'),
    path('get-unread-count/', views.GetUnreadCountView.as_view(), name='get_unread_count'),
]