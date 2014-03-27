"""
#TODO: Add module docstring
"""
import re

from django_crucrudile.utils import get_dashed_name

class ModelActionMixin(object):
    """
    #TODO: Add class docstring
    """
    @classmethod
    def get_action_name(cls):
        """
        #TODO: Add method docstring
        """
        class_name = cls.__name__
        camel_cased_name = class_name[:-4] if class_name.endswith('View') else class_name
        return get_dashed_name(camel_cased_name)

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
