"""
#TODO: Add module docstring
"""
from django.template import Library

register = Library() #pylint: disable=C0103

@register.filter
def multiply(first_term, second_term):
    """
    #TODO: Add method docstring
    """
    return first_term * second_term
