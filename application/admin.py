from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from application.models.user import Moderator, UserForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView

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