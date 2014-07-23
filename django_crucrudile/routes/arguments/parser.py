from abc import ABCMeta, abstractmethod
from functools import partial, reduce
from itertools import product


def combine(iterable, separator):
    return separator.join(filter(None, iterable))


def compose(functions, args=None, kwargs=None):
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    def pass_args(func):
        return partial(func, *args, **kwargs)

    def inner_compose(f, g):
        f = pass_args(f)
        g = pass_args(g)
        return lambda x: f(bg(x))

    return reduce(
        inner_compose,
        functions
    )


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

        super().__init__(self.parse_regexs(regexs))

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

    @abstractmethod
    def parse_regexs(self, regexs):
        pass

class ArgParser(BaseArgParser):
    """Route URL arguments specification. Generates argument regexes from
    a given argument specification. This allows you to give the possible
    URL arguments to be used in the URL, and :func:`get_regexs` will
    return a regex for each argument combination found.

    """
    def transform_to_tuple(self, items):
        for item in items:
            if not isinstance(item, tuple):
                yield None, item
            else:
                yield item


    def apply_required_default(self, items):
        for required, args in items:
            if required is None:
                required = self.redirect_default
            yield required, args


    def mark_required(self, items):
        for required, args in items:
            if required:
                self.required = True
            yield required, args


    def transform_args_to_list(self, items):
        for required, args in items:
            if isinstance(args, str):
                args = [args, ]
            yield required, args


    def cartesian_product(self, items):
        combs = [None]

        for required, args in items:
            sep = self.get_separator(required)
            combs = map(
                partial(combine, sep=sep),
                product(combs, args)
            )

        return combs


    regexs_filters = [
        transform_to_tuple,
        apply_required_default,
        mark_required,
        transform_args_to_list,
        cartesian_product
    ]


    def parse_regexs(self, specs):
        filters = compose(self.regexs_filters, self)
        return map(filters, specs)
