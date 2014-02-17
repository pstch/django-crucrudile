from .auth import AuthMixin
from .context import ExtraContextMixin, ModelInfoMixin
from .redirect import ModelFormRedirectMixin
from .template import TemplateMixin

class BaseMixins(AuthMixin, ExtraContextMixin, TemplateMixin):
    pass

class BaseModelMixins(BaseMixins, ModelInfoMixin):
    pass

class BaseModelFormMixins(BaseModelMixins, ModelFormRedirectMixin):
    pass
