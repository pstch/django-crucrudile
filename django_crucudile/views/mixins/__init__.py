"""
#TODO: Add module docstring
"""
from django_crucrudile.utils import get_underscored_name, get_dashed_name

class ModelActionMixin(object):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_camel_cased_action_name(cls):
        """
        #TODO: Add method docstring
        """
        class_name = cls.__name
        if class_name.endswith('View'):
            return class_name[:-4]
        else:
            return class_name
    @classmethod
    def get_dashed_action_name(cls):
        """
        #TODO: Add method docstring
        """
        return get_dashed_name(cls.get_camel_cased_action_name())
    @classmethod
    def get_underscored_action_name(cls):
        """
        #TODO: Add method docstring
        """
        return get_underscored_name(cls.get_camel_cased_action_name())
    @classmethod
    def get_action_name(cls):
        """
        #TODO: Add method docstring
        """
        return cls.get_dashed_action_name()
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
        url_part = [cls.get_action_name()]
        url_part += cls.get_url_args()
        return "/".join(url_part)
