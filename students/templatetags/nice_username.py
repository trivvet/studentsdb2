# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter
def nice_username(user_object):
    """Get full name or username from user object"""
    if len(user_object.get_full_name()) < 10:
        value = user_object.get_full_name()
    else:
        value = user_object.get_short_name()
    if value == '':
        value = user_object.get_username()
    return value
