from django.core.exceptions import PermissionDenied
from application.models.spaces import Space,Owners


def user_is_autorized(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser:
            return function(request, *args, **kwargs)
        space = Space.objects.get(pk=kwargs['space_id'])
        owners = Owners.objects.filter(space=kwargs['space_id'],user=request.user.id)
        print('hola')
        print(space.province.lower())
        print(request.user.moderator.province.lower())
        if owners.count()>0:
            return function(request, *args, **kwargs)
        if(request.user.moderator.is_moderator or request.user.moderator.is_country_moderator):
                if space.province.lower() == request.user.moderator.province.lower():
                    return function(request, *args, **kwargs)
                if(space.country == request.user.moderator.country):
                    return function(request, *args, **kwargs)
        raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
