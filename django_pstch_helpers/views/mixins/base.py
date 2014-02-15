from .auth import AuthMixin
from .context import ExtraContextMixin, ModelInfoMixin
from .redirect import ModelFormRedirectMixin

class BaseMixins(AuthMixin, ExtraContextMixin):
    pass

class BaseModelMixins(BaseMixins, ModelInfoMixin):
    pass

class BaseModelFormMixins(BaseModelMixins, ModelFormRedirectMixin):
    pass
