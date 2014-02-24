"""
#TODO: Write module docstring
"""
from .auth import AuthMixin
from .context import ExtraContextMixin, ModelInfoMixin
from .redirect import ModelFormRedirectMixin
from .template import TemplateResponseMixin, SingleObjectTemplateResponseMixin

#pylint: disable=R0901

class BaseMixins(AuthMixin,
                 ExtraContextMixin,
                 TemplateResponseMixin):
    """
    #TODO: Write class docstring
    """
    pass

class BaseModelMixins(BaseMixins,
                      ModelInfoMixin,
                      SingleObjectTemplateResponseMixin):
    """
    #TODO: Write class docstring
    """
    pass

class BaseModelFormMixins(BaseModelMixins, ModelFormRedirectMixin):
    """
    #TODO: Write class docstring
    """
    pass
