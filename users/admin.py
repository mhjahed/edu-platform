from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fieldsets = (
        ('Role Information', {
            'fields': ('role',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Examiner Details', {
            'fields': ('position', 'profession'),
            'classes': ('collapse',)
        }),
        ('Student Details', {
            'fields': ('school', 'class_grade', 'group', 'whatsapp'),
            'classes': ('collapse',)
        })
    )

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = [
        'username', 'email', 'first_name', 'last_name', 
        'role_display', 'is_active', 'date_joined'
    ]
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'date_joined',
        'profile__role'
    ]
    search_fields = [
        'username', 'first_name', 'last_name', 'email',
        'profile__phone', 'profile__school'
    ]
    
    def role_display(self, obj):
        try:
            role = obj.profile.role
            if role == 'Examiner':
                return format_html('<span style="color: blue; font-weight: bold;">👨‍🏫 Examiner</span>')
            elif role == 'Candidate':
                return format_html('<span style="color: green; font-weight: bold;">🎓 Student</span>')
            else:
                return format_html('<span style="color: gray;">No Role</span>')
        except:
            return format_html('<span style="color: red;">No Profile</span>')
    role_display.short_description = 'Role'
    
    actions = ['make_examiner', 'make_candidate', 'activate_users', 'deactivate_users']
    
    def make_examiner(self, request, queryset):
        for user in queryset:
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = 'Examiner'
            profile.save()
        self.message_user(request, f"Set {queryset.count()} users as Examiners.")
    make_examiner.short_description = "Set selected users as Examiners"
    
    def make_candidate(self, request, queryset):
        for user in queryset:
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = 'Candidate'
            profile.save()
        self.message_user(request, f"Set {queryset.count()} users as Candidates.")
    make_candidate.short_description = "Set selected users as Candidates"
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Activated {updated} users.")
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"Deactivated {updated} users.")
    deactivate_users.short_description = "Deactivate selected users"

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'role', 'phone', 'email', 'school', 
        'position'
    ]
    list_filter = [
        'role', 'school', 'class_grade', 'group'
    ]
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name',
        'phone', 'email', 'school', 'position'
    ]
    readonly_fields = []
    date_hierarchy = None
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Examiner Information', {
            'fields': ('position', 'profession'),
            'classes': ('collapse',)
        }),
        ('Student Information', {
            'fields': ('school', 'class_grade', 'group', 'whatsapp'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['change_role_to_examiner', 'change_role_to_candidate']
    
    def change_role_to_examiner(self, request, queryset):
        updated = queryset.update(role='Examiner')
        self.message_user(request, f"Changed {updated} profiles to Examiner role.")
    change_role_to_examiner.short_description = "Change to Examiner role"
    
    def change_role_to_candidate(self, request, queryset):
        updated = queryset.update(role='Candidate')
        self.message_user(request, f"Changed {updated} profiles to Candidate role.")
    change_role_to_candidate.short_description = "Change to Candidate role"

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
