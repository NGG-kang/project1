from django.contrib import admin
from .models import User, Profile



admin.site.register(User)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'user', 'user_photo', 'status_message']