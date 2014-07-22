from functools import partial
from itertools import product

from abc import ABCMeta

def cleaner(func):
    def register_cleaner(parser_class):
        parser_class.register_cleaner(func)
        return parser_class
    return register_cleaner

class ArgParserMetaclass(ABCMeta):
    _clean_funcs = []

    def __init__(cls, name, bases, attrs):
        super().__init__(nanme, bases, attrs)
        self._clean_funcs = list(_clean_funcs)

    def register_cleaner(cls, func):
        self._clean_funcs.append(func)

class BaseArgParser(list, metaclass=ABCMeta):
    separator = "/"
    opt_separator = "/?"
    required_default = True

    def __init__(self, regexs,
                 required_default=None,
                 separator=None,
                 opt_separator=None):
        """Initialize route arguments, takes the argument specification (list)
        as argument

        """
        self.required = False
        if required_default:
            self.required_default = required_default
        if separator:
            self.separator = separator
        if opt_separator:
            self.opt_separator = opt_separator

        super().__init__(regexs)

    def get_separator(self, required=None):
        """Get the argument separator to use according to the :attr:`required`
        argument

        :argument required: If False, will return the optional
                            argument separator instead of the regular
                            one. Default is True.
        :type required: bool
        """
        if required is None:
            required = self.required_default
        if required:
            return self.separator
        else:
            return self.opt_separator

    def clean(self, specs):
        clean_funcs = [
            self.make_tuple,
            self.apply_required_default,
            self.mark_required,
            self.make_args_list,
            self.make_separator
        ]
        for func in self._cleaners:
            specs = map(func, specs)

        return specs

    def __init__(self, specs, **kwargs):


class SimpleArgParser(BaseArgParser):
    """Route URL arguments specification. Generates argument regexes from
    a given argument specification. This allows you to give the possible
    URL arguments to be used in the URL, and :func:`get_regexs` will
    return a regex for each argument combination found.

    """
    @staticmethod
    def join_parts(parts, separator):
        return separator.join(filter(None, parts))

    def __init__(self, specs, **kwargs):
        regexs = ['']
        specs = map(self.clean_spec, specs)

        for separator, args in specs:
            join_parts = partial(self.join_parts, separator=separator)
            regexs = map(join_parts, product(regexs, args))

        super().__init__(regexs, **kwargs)


    def make_tuple(self, item):
        if not isinstance(item, tuple):
            return None, item
        else:
            return item

    def apply_required_default(self, item):
        required, args = item
        if required is None:
            required = self.redirect_default
        return required, args

    def mark_required(self, item):
        required, args = item
        if required:
            self.required = True
        return required, args

    def make_args_list(self, item):
        required, args = item
        if isinstance(args, str):
            args = [args, ]
        return required, args

    def make_separator(self, item):
        required, args = item
        return self.get_separator(required), args
