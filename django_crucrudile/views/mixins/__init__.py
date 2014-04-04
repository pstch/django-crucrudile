"""
#TODO: Add module docstring
"""
from django_crucrudile.utils import convert_camel_case

class ModelActionMixin(object):
    """
    #TODO: Add class docstring
    """
    action = None

    @classmethod
    def get_fallback_action_name(cls):
        """
        #TODO: Add method docstring
        """
        class_name = cls.__name__
        if class_name.endswith('View'):
            class_name = class_name[:-4]
        return convert_camel_case(class_name, '-')

    @classmethod
    def get_action_name(cls):
        """
        #TODO: Add method docstring
        """
        return cls.action or cls.get_fallback_action_name()

    @classmethod
    def get_underscored_action_name(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_action_name().replace('-', '_')

    @classmethod
    def get_url_args(cls):
        """
        #TODO: Add method docstring
        """
        return []

    @classmethod
    def get_url_part(cls):
        """
        #TODO: Add method docstring
        """
        url_part = [cls.get_action_name()] + cls.get_url_args()
        return "/".join(url_part)
