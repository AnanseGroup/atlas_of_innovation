from django.core.exceptions import PermissionDenied
from application.models.spaces import Space,Owners
from itertools import chain
from django.contrib.auth.models import Permission

def user_is_autorized_in_Space(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        space = Space.objects.get(pk=kwargs['space_id'])
        owners = Owners.objects.filter(space=kwargs['space_id'],user=request.user.id)
       
        if owners.count()>0:
            return function(request, *args, **kwargs)
        if(request.user.moderator.is_moderator):
                if space.province.lower() == request.user.moderator.province.lower():
                    return function(request, *args, **kwargs)
        if request.user.moderator.is_country_moderator:
                if(space.country == request.user.moderator.country):
                    return function(request, *args, **kwargs)
        raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_autorized_to_upload(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        if not (request.user.moderator.is_moderator or request.user.moderator.is_country_moderator):
            raise PermissionDenied
        if list(set(chain(request.user.user_permissions.filter(codename='upload_provisonal_spaces').values_list('codename', flat=True), Permission.objects.filter(group__user=request.user, codename='upload_provisonal_spaces').values_list('codename', flat=True)))):
            return function(request, *args, **kwargs)
        raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
def user_is_autorized_to_analize(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        if not (request.user.moderator.is_moderator or request.user.moderator.is_country_moderator):

            raise PermissionDenied
        if list(set(chain(request.user.user_permissions.filter(codename='analyse_provisional_spaces').values_list('codename', flat=True), Permission.objects.filter(group__user=request.user, codename='analyse_provisional_spaces').values_list('codename', flat=True)))):
            
            return function(request, *args, **kwargs)
        
        raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap