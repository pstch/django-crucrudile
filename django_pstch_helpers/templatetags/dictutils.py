from django import template
from django.conf import settings
register = template.Library()

@register.filter
def keyvalue(dict, key):
        return dict.get(key) if dict else None