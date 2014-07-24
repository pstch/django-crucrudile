from .. import BaseRoute
from .builder import ArgsBuilder


__all__ = ["ArgumentsMixin", "ArgBuilder"]


class ArgumentsMixin(BaseRoute):
    arguments_spec = []
    arguments_builder = ArgsBuilder


    def __init__(self, *args,
                 arguments_spec=None, arguments_builder=None,
                 **kwargs):
        """Initialize Route, check that needed attributes/arguments are
        defined.

        """
        if arguments_spec is not None:
            self.arguments_spec = arguments_spec
        if arguments_builder is not None:
            self.arguments_builder = arguments_builder

        self.arguments = self.arguments_builder(self.arguments_spec)

        super().__init__(*args, **kwargs)


    def get_url_specs(self):
        for prefix, name, suffix in super().get_url_specs():
            if self.arguments:
                for arg in self.arguments:
                    yield prefix, name, suffix + arg
