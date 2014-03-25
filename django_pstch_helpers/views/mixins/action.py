"""
#TODO: Add module docstring
"""

class ActionMixin(object):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_action_name(cls):
        def get_dashed_name(camel_cased):
            """
            #TODO: Add method docstring
            """
            step = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', camel_cased)
            return re.sub('([a-z0-9])([A-Z])', r'\1-\2', step).lower()

        """
        #TODO: Add method docstring
        """
        class_name = cls.__name__
        camel_cased_name = class_name[:-4] if class_name.endswith('View') else class_name
        return get_dashed_name(camel_cased_name)
