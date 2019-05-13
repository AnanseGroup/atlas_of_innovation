from django import template 
from application.models import ProvisionalSpace

register = template.Library()
 
@register.simple_tag
def get_provisional_sum():
    sum = ProvisionalSpace.objects.count()
    print(sum)
    return sum 