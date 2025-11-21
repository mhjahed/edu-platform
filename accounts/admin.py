from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {
            'fields': ('role', 'phone_number', 'date_of_birth', 'profile_picture', 'bio')
        }),
        ('Student Information', {
            'fields': ('student_id', 'institution'),
            'classes': ('collapse',)
        }),
        ('Examiner Information', {
            'fields': ('department', 'employee_id'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {
            'fields': ('role', 'email', 'phone_number')
        }),
    )


admin.site.register(User, UserAdmin)
