"""
Utility functions
"""
def convert_camel_case(camel_cased, separator):
    separator_expression = r'\1%s\2' % separator
    step = re.sub('(.)([A-Z][a-z]+)',
                  separator_expression,
                  camel_cased)
    return re.sub('([a-z0-9])([A-Z])',
                  separator_expression,
                  step).lower()

def get_dashed_name(camel_cased):
    """
    #TODO: Add method docstring
    """
    return convert_camel_case(camel_cased, '-')

def get_underscored_name(camel_cased):
    """
    #TODO: Add method docstring
    """
    return convert_camel_case(camel_cased, '_')

def make_url_name(namespaces, object_url_name, action):
    """
    Joins namespaces with an action and optionally an URL name

    Will return "<namespaces>:<object_url_name>-<action>" if
    object_url_name is not None, otherwise "<namespaces>:<action>"
    (without '<>').
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
