"""Utility functions meant for use in 'urls.py', to create URL
patterns

"""
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
