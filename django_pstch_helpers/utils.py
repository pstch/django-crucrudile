"""
Utility functions for django-pstch-helpers
"""
#pylint: disable=W0142
def get_filter_class(filter_model, filter_class):
    """
    Utility function to create a django-filter FilterClass with a
    specific model.

    We need this because we want to create filters dynamically to
    include them in models.py
    """
    class FilterSet(filter_class):
        #pylint: disable=W0232, R0903, C0111
        lookup_type = None
        class Meta(filter_class.Meta):
            model = filter_model
    return FilterSet

def make_url_name(namespaces, object_url_name, action):
    """
    Joins namespaces with an action and optionally an URL name

    Will return "<namespaces>:<object_url_name>-<action>" if
    object_url_name is not None, otherwise "<namespaces>:<action>"
    (without the '<>').
    """
    def _namespaces():
        "Join namespaces together for the left part of the URL name"
        return ":".join(
            namespaces if namespaces else []
        )
    def _short_url_name():
        "Join object_url_name and action for the right part of the URL name"
        return "-".join(
            [object_url_name, action] if object_url_name else [action]
        )
    return  ":".join([
        _namespaces(),
        _short_url_name()
    ]) if namespaces else _short_url_name()
