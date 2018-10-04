from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter
def obfuscate_email(value): # Only one argument.
    m = value.split('@')
    f = m[0][0]+"".join(['*' for a in m[0][1:-1]])+m[0][-1]+"@"+m[1][0]+"".join(['*' for a in m[1][1:-1]])+m[1][-1]
    return f

@register.filter
def obfuscate_phone(value): # Only one argument.
    f = "".join(['*' for a in value[:-2]])+value[-2:]
    return f