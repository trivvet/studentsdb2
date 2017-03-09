from django import template

register = template.Library()

@register.filter
def nice_username(user_object):
    """Get full name or username from user object"""
    value = user_object.get_full_name()
    if value == '':
        value = user_object.get_username()
    return value
