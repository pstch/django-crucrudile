from .parser import ArgParser


__all__ = ["ArgumentsMixin", "ArgParser"]


class ArgumentsMixin:
    arguments_spec = []
    arguments_parser = ArgParser

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

        self.arguments = self.arguments_parser(self.arguments_spec)

        super().__init__(*args, **kwargs)

    def clean_url_part(self, url_part=None):
        if url_part is not None:
            part = url_part
        else:
            part = self.url_part
        if part:
            return '/' + part
        else:
            return ''

    def make_url_regexs(self, url_part=None):
        return super().make_url_regexs(url_part)
        part = self.clean_url_part(url_part)

    def foo():
        if self.arguments:
            for arg in self.arguments:
                yield '^{}$'.format(
                    self.arguments.get_separator().join(
                        filter(None, [part, arg])
                    )
                )
        else:
            return super().make_url_regexs(url_part)
