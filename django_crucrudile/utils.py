"""
Utility functions
"""
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
