from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from application.models.user import Moderator

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ModeratorInline(admin.StackedInline):
    model = Moderator
    can_delete = False
    verbose_name_plural = 'moderators'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ModeratorInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)