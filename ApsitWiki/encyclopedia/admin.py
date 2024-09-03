from django.contrib import admin
from .models import *
# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date')  # Fields to display in the list view
    search_fields = ('user__username', 'bio', 'location')     # Fields to include in search
admin.site.register(UserProfile, UserProfileAdmin) 