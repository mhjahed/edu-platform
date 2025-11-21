from django.contrib import admin
from django.utils.html import format_html
from .models import Message, Request

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'subject', 'sender', 'receiver', 'message_type', 
        'exam', 'sent_at', 'is_read_display'
    ]
    list_filter = [
        'message_type', 'sent_at', 'is_read', 'exam'
    ]
    search_fields = [
        'subject', 'body', 'sender__username', 
        'receiver__username', 'exam__title'
    ]
    readonly_fields = ['sent_at']
    date_hierarchy = 'sent_at'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('sender', 'receiver', 'subject', 'body', 'message_type')
        }),
        ('Related Exam', {
            'fields': ('exam',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_read', 'sent_at')
        })
    )
    
    def is_read_display(self, obj):
        if obj.is_read:
            return format_html('<span style="color: green; font-weight: bold;">✓ Read</span>')
        else:
            return format_html('<span style="color: orange; font-weight: bold;">⏳ Unread</span>')
    is_read_display.short_description = 'Status'
    
    actions = ['mark_as_read', 'mark_as_unread', 'send_reply']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"Marked {updated} messages as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"Marked {updated} messages as unread.")
    mark_as_unread.short_description = "Mark selected messages as unread"

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = [
        'subject', 'student', 'exam', 'status', 'created_at', 
        'replied_at', 'replied_by_display'
    ]
    list_filter = [
        'status', 'created_at', 'replied_at', 'exam'
    ]
    search_fields = [
        'subject', 'message', 'student__username', 
        'student__first_name', 'student__last_name', 'exam__title'
    ]
    readonly_fields = ['created_at', 'replied_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Request Information', {
            'fields': ('student', 'exam', 'subject', 'message', 'status')
        }),
        ('Reply Information', {
            'fields': ('reply', 'replied_by', 'replied_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def replied_by_display(self, obj):
        if obj.replied_by:
            return format_html('<span style="color: green; font-weight: bold;">✓ {}</span>', obj.replied_by.username)
        else:
            return format_html('<span style="color: orange; font-weight: bold;">⏳ No Reply</span>')
    replied_by_display.short_description = 'Replied By'
    
    actions = ['mark_as_replied', 'mark_as_resolved', 'mark_as_pending']
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(status='replied', replied_by=request.user)
        self.message_user(request, f"Marked {updated} requests as replied.")
    mark_as_replied.short_description = "Mark selected requests as replied"
    
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(status='resolved')
        self.message_user(request, f"Marked {updated} requests as resolved.")
    mark_as_resolved.short_description = "Mark selected requests as resolved"
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f"Marked {updated} requests as pending.")
    mark_as_pending.short_description = "Mark selected requests as pending"
