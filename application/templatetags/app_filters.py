from django import template
from datetime import date, timedelta
from application.models import ProvisionalSpace
from itertools import chain
from django.contrib.auth.models import Permission
import re
from django.conf import settings
from application.models import Space
from application.views import IsOwner
register = template.Library()

@register.filter
def hide_email(value):
    m = value.split('@')
    f = m[0][0]+"".join(['*' for a in m[0][1:-1]])+m[0][-1]+"@"+m[1][0]+"".join(['*' for a in m[1][1:-1]])+m[1][-1]
    return f

@register.filter
def hide_phone(value):
    f = "".join(['*' for a in value[:-2]])+value[-2:]
    return f

@register.simple_tag
def get_provisional_sum():
    sum = ProvisionalSpace.objects.count()
    return sum

@register.filter
def check_permission(user, permission):
    ''' Compares the user permissions if it matches or is superuser returns true
    '''
    if user.is_superuser:
        return True
    if user.is_anonymous:
        return False
    ''' This looks a little bit complicated but it's basically getting all the 
        user and group permissions to see if it matches the permission string and
        returns a list
    '''
    perm_list = list(set(chain(user.user_permissions.filter(codename=permission).values_list('codename', flat=True), Permission.objects.filter(group__user=user, codename=permission).values_list('codename', flat=True))))
    if perm_list:
        return True
    return False
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    numeric_test = re.compile("^\d+$")
    if hasattr(value, str(arg)):
       if value._meta.get_field(arg).get_internal_type()=='ManyToManyField':
         value=getattr(value,arg).first()
         print(value)
         if value is not None:
            return value.name 
         else:
            return value  
       else:
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID
register.filter('getattribute', getattribute)
@register.filter
def ExistSpaces(arg):
    query=Space.objects.filter(country=arg)
    if query.first() is not None:
     return True
    else:
        return False
@register.filter
def isAuthorized(user,space):
    print(space.province.lower())
    print(user.moderator.province.lower())
    if IsOwner(user.id,space.id):
       return True
    if(user.moderator.is_moderator or user.moderator.is_country_moderator):
            if space.province.lower() == user.moderator.province.lower():
                    return True
            if(space.country == user.moderator.country):
                    return True
    return False
@register.filter
def moderateThisSpace(user_id,country,province):
    user=User.objects.get(id=user_id)
    moderator=Moderator.objects.get(user=user)
    if moderator.is_moderator:
        if moderator.province.lower()==province.lower():
           return True
    if moderator.is_country_moderator:
        if moderator.country == country:
            return True
    return False


