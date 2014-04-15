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

from django.core.exceptions import ImproperlyConfigured

def auto_patterns_for_app(app_name, exclude_models=None):
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

    urlpatterns = []
    exclude_models = exclude_models or []
    content_types = ContentType.objects.filter(app_label=app_name)
    models = [content_type.model_class() for content_type in content_types]

    for model in models:
        if model.__name__ not in exclude_models:
            for pattern in model.get_url_patterns():
                urlpatterns.append(pattern)

    return urlpatterns

def try_calling(arg, *args, **kwargs):
    """Evaluate and return arg (with given args and kwargs) if it's a
    callable, otherwise return None

    """
    return arg(*args, **kwargs) if callable(arg) else None

def convert_camel_case(camel_cased, separator):
    """Convert camel cased into words separated by the given separator

    Keywords : -- camel_cased (ex:"CamelCased") -- separator (ex:"-")

    Above parameters will return "camel-cased"

    """
    separator_expression = r'\1%s\2' % separator
    step = re.sub('(.)([A-Z][a-z]+)',
                  separator_expression,
                  camel_cased)
    return re.sub('([a-z0-9])([A-Z])',
                  separator_expression,
                  step).lower()

def _is_special_attribute(attr):
    """Return True if attr is a Python special attribute, otherwise
    False"""
    return \
        not attr.startswith('__') and \
        not attr.endswith('__')

def monkeypatch_mixin(class_, mixin):
    """Monkeypatch all non-special (bound and unbound) attributes of mixin
into class_, then return class_"""
    for attr in dir(mixin):
        if not _is_special_attribute(attr) and \
           not hasattr(class_, attr):
            # we found a non-special attribute in ModeActionMixin
            # that is not present in view_class
            # let's monkeypatch it to class_
            setattr(
                class_,
                attr,
                mixin.__dict__[attr]
            )
            # we use .__dict__[] because we need unbound
            # attributes
    return class_
