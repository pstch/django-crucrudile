"""
Utility functions
"""
import re

from django.core.exceptions

def auto_patterns_for_app(app_name):
    try:
        from django.contrib.contenttypes.models import ContentType
    except ImportError:
        raise Improperlyconfigured("auto_patterns_for_app must be able to import django.contrib.contenttypes")
    return ContentType.objects.filter(app_label=app_name)

def auto_patterns(content_types):
    patterns = []
    for content_type in content_types:
        patterns += content_type.model_class().get_url_patterns()
    return patterns

def call_if_needed(arg, *args, **kwargs):
    return arg if not callable(arg) else arg(*args, **kwargs)


def convert_camel_case(camel_cased, separator):
    """
    #TODO: Add method docstring
    """
    separator_expression = r'\1%s\2' % separator
    step = re.sub('(.)([A-Z][a-z]+)',
                  separator_expression,
                  camel_cased)
    return re.sub('([a-z0-9])([A-Z])',
                  separator_expression,
                  step).lower()
