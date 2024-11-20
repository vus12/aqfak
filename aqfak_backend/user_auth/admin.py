from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


# admin.site.register(Crop)
# admin.site.register(CropSensorData)
# admin.site.register(CropSchedule)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define which fields should be displayed in the admin interface
    list_display = ('username', 'email', 'name', 'place'
    )
    
    # Add support for editing custom fields in forms
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profilePhoto', 'name', 'place')}),
    )
