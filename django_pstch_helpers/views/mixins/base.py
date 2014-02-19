from .auth import AuthMixin
from .context import ExtraContextMixin, ModelInfoMixin
from .redirect import ModelFormRedirectMixin
from .template import TemplateResponseMixin, SingleObjectTemplateResponseMixin

class BaseMixins(AuthMixin, ExtraContextMixin, TemplateResponseMixin):
    pass

class BaseModelMixins(SingleObjectTemplateResponseMixin, BaseMixins, ModelInfoMixin):
    pass

class BaseModelFormMixins(BaseModelMixins, ModelFormRedirectMixin):
    pass
