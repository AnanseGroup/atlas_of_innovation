from django import template 
from application.models import ProvisionalSpace

register = template.Library()
 
@register.filter
def get_provisional_sum(user):
    if user.is_superuser:
 #       print('superuser')
        return ProvisionalSpace.objects.count()
    if user.moderator.is_country_moderator:
#        print('is country moderator')
        sum = ProvisionalSpace.objects.filter(country=user.moderator.country).count()
    else:
#        print('is province moderator')
        sum = ProvisionalSpace.objects.filter(country=user.moderator.country,province=user.moderator.province).count()
#    print(sum)
    return sum 