from django import template
from datetime import date, timedelta
from urllib.parse import urlparse, ParseResult

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

@register.filter
def http_in_url(value):
    '''Adds http to an url in case is not present in the string
    '''
    p = urlparse(value, 'http')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    p = ParseResult('http', netloc, path, *p[3:])
    f = p.geturl()
    return f
