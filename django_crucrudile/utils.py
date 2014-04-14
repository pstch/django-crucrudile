"""Utility functions

Imports :
 -- re : needed by convert_camel_case
 -- django...ImproperlyConfigured : might be raised by auto_patterns_for_app
 -- itertools.chain : needed by auto_patterns_for_app (to join lists)

Functions :
 -- auto_patterns_for_app(app_name)
 -- auto_patterns_for_model(model)
 -- try_calling(arg, *args, **kwargs)
 -- convert_camel_case(camel_cased, separator)

"""
import re
from itertools import chain

from django.core.exceptions import ImproperlyConfigured

def auto_patterns_for_app(app_name, exclude_models = None):
    """Returns a list of URL patterns (Django URL objects) for the given
    application, using content types.

    This function will try to import django.contrib.contenttypes, and
    fail if it can't.
    """
    try:
        from django.contrib.contenttypes.models import ContentType
    except ImportError: #pragma: no cover
        raise ImproperlyConfigured(
            "auto_patterns_for_app must be able to import"
            " django.contrib.contenttypes"
        )

    content_types = ContentType.objects.filter(app_label=app_name)
    urlpatterns = []

    for ct in content_types:
        model = ct.model_class()
        if not exclude_models or \
           (exclude_models and model.__name__ not in exclude_models):
            for pattern in model.get_url_patterns():
                urlpatterns.append(pattern)

    return urlpatterns

def try_calling(arg, *args, **kwargs):
    """Evaluate and return arg if it's a callable, otherwise return None
    """
    return arg(*args, **kwargs) if callable(arg) else None

def supple_join(separator, items):
    """Joins items with separator, excluding items that are None

    Example: _supple_join([1, 2, 0, 3], '-') -> '1-2-3'
    """
    return separator.join(filter(None, items))

def convert_camel_case(camel_cased, separator):
    """Convert camel cased into words separated by the given separator

    Keywords :
    -- camel_cased (ex:"CamelCased")
    -- separator (ex:"-")

    Above parameters will return "camel-cased"
    """
    separator_expression = r'\1%s\2' % separator
    step = re.sub('(.)([A-Z][a-z]+)',
                  separator_expression,
                  camel_cased)
    return re.sub('([a-z0-9])([A-Z])',
                  separator_expression,
                  step).lower()
