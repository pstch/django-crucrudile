from django import template
from django.conf import settings
register = template.Library()

@register.filter
def multiply(a, b):
        return a * b