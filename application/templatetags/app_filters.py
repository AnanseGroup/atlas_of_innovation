from django import template
from datetime import date, timedelta
from application.models import ProvisionalSpace
from itertools import chain
from django.contrib.auth.models import Permission


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
