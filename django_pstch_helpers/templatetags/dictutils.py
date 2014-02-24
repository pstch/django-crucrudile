"""
#TODO: Add module docstring
"""
from django.template import Library

register = Library() #pylint: disable=C0103

@register.filter
def keyvalue(dictionary, key):
    """
    #TODO: Add method docstring
    """
    return dictionary.get(key) if dict else None
