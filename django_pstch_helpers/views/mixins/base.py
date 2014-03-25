"""
#TODO: Write module docstring
"""

from .action import ActionMixin
from .auth import AuthMixin
from .context import ExtraContextMixin, ModelInfoMixin
from .redirect import ModelFormRedirectMixin
from .template import TemplateResponseMixin, SingleObjectTemplateResponseMixin

#pylint: disable=R0901

class BaseViewMixins(AuthMixin,
                     ExtraContextMixin,
                     TemplateResponseMixin):
    """
    #TODO: Write class docstring
    """
    pass

class BaseModelViewMixins(BaseViewMixins,
                          ModelInfoMixin,
                          SingleObjectTemplateResponseMixin):
    """
    #TODO: Write class docstring
    """
    pass

class BaseModelFormViewMixins(BaseModelViewMixins,
                              ModelFormRedirectMixin):
    """
    #TODO: Write class docstring
    """
    pass
