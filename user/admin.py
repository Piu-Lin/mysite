from django.contrib import admin
from .models import Profile


from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class PorfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (PorfileInline,)
    list_display=('username','nickname','email','is_staff','is_active','is_superuser')
    def nickname(self,obj):
        return obj.profile.nickname
    nickname.short_description='昵称'
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)





@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','nickname')