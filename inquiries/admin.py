from django.contrib import admin
from .models import Inquiry, InquiryMessage


class InquiryMessageInline(admin.TabularInline):
    model = InquiryMessage
    extra = 0
    readonly_fields = ['created_at']
    fields = ['sender', 'message', 'is_read', 'created_at']
    ordering = ['-created_at']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'recipient', 'exam', 'status', 'priority', 'message_count', 'created_at']
    list_filter = ['status', 'priority', 'created_at', 'exam']
    search_fields = ['subject', 'sender__username', 'recipient__username', 'exam__exam_code']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Inquiry Details', {
            'fields': ('subject', 'sender', 'recipient', 'exam')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'resolved_at')
        }),
    )
    
    inlines = [InquiryMessageInline]
    
    actions = ['mark_resolved', 'mark_in_progress']
    
    def message_count(self, obj):
        return obj.message_count
    message_count.short_description = 'Messages'
    
    def mark_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='resolved', resolved_at=timezone.now())
        self.message_user(request, f"{queryset.count()} inquiries marked as resolved.")
    mark_resolved.short_description = "Mark selected inquiries as resolved"
    
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f"{queryset.count()} inquiries marked as in progress.")
    mark_in_progress.short_description = "Mark selected inquiries as in progress"


@admin.register(InquiryMessage)
class InquiryMessageAdmin(admin.ModelAdmin):
    list_display = ['inquiry', 'sender', 'message_preview', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at', 'inquiry__status']
    search_fields = ['inquiry__subject', 'sender__username', 'message']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message Preview'
