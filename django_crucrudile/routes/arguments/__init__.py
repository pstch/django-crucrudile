from .. import BaseRoute
from .parser import ArgumentsParser


__all__ = ["ArgumentsMixin", "ArgParser"]


class ArgumentsMixin(BaseRoute):
    arguments_spec = []
    arguments_parser = ArgumentsParser


    def __init__(self, *args,
                 arguments_spec=None, arguments_parser=None,
                 **kwargs):
        """Initialize Route, check that needed attributes/arguments are
        defined.

        """
        if arguments_spec is not None:
            self.arguments_spec = arguments_spec
        if arguments_parser is not None:
            self.arguments_parser = arguments_parser

        parser = self.arguments_parser(self.arguments_spec)
        self.arguments = parser()

        super().__init__(*args, **kwargs)


    def get_url_specs(self):
        for prefix, name, suffix in super().get_url_specs():
            if self.arguments:
                for arg in self.arguments:
                    yield prefix, name, suffix + [arg]
