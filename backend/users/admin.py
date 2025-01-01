from django.contrib import admin
from .models import CustomUserModel


class CustomUserAdmin(admin.ModelAdmin):
    """
    CustomUserAdmin is a custom admin interface for the User model.
    Attributes:
        list_display (list): Fields to display in the admin list view.
        search_fields (list): Fields to include in the search functionality.
        list_filter (list): Fields to include in the filter sidebar.
        fieldsets (tuple): Configuration for grouping fields in the admin form.
    Methods:
        get_queryset(request):
            Returns a queryset filtered by the user's region if the user is not a superuser.
        save_model(request, obj, form, change):
            Sets a default password for new users before saving the model.
    """
    list_display = ['username', 'email', 'phoneNumber', 'address', 'region', 'city', 'country']
    search_fields = ['username', 'email', 'phoneNumber', 'city']
    list_filter = ['region', 'city']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('phoneNumber', 'address', 'region', 'city', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(region=request.user.region)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password('default_password')
        super().save_model(request, obj, form, change)
    
