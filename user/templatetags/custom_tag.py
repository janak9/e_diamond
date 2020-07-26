from django import template

register = template.Library()

@register.filter(name='sub')
def sub(value, arg):
    return value - arg

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='ifinlist')
def ifinlist(value, list):
    return True if str(value) in list else False