from copy import copy
from itertools import chain
from functools import reduce, partial, wraps

def pass_tuple(count=1):
    def decorator(func):
        @wraps(func)
        def decorated(args_tuple, *args, **kwargs):
            return args_tuple[:count] + (
                func(
                    *args_tuple[count:] + args,
                    **kwargs
                ),
            )
        return decorated
    return decorator


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
        def composed(x):
            return f(g(x))
        return composed

    return reduce(
        inner_compose,
        functions
    )


class Separated:
    separator = "/"
    opt_separator = "/?"
    required_default = True

    def __init__(self,
                 *args,
                 separator=None,
                 opt_separator=None,
                 required_default=None,
                 **kwargs):
        """Initialize route arguments, takes the argument specification (list)
        as argument

        """
        self.required = False
        if separator:
            self.separator = separator
        if opt_separator:
            self.opt_separator = opt_separator
        if required_default:
            self.required_default = required_default

        super().__init__(*args, **kwargs)


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
            return self.opppt_separator

class Parsable:
    def __add__(self, other):
        if not other:
            return self

        new = copy(self)

        if isinstance(other, list):
            new.extend(other)
        else:
            new.append(other)

        return new

    def get_filters(self):
        return []

    def __call__(self, items=None):
        if items is None:
            items = self

        filters = self.get_filters()
        composed_filters = compose(reversed(filters))
        # tuple (bool, str or list (str))
        # or str or list (tuple (bool, str or list (str)) or str)
        # ->
        # iterable(str)
        return composed_filters(items)

    def apply_filters(self, items=None):
        return self(items)


class OptionalPartList(Separated, Parsable, list):
    def __init__(self, iterable=None,
                 separator=None, opt_separator=None, required_default=None):
        # allow directly creating empty lists
        if iterable is None:
            iterable = []

        super().__init__(
            iterable,
            separator=separator,
            opt_separator=opt_separator,
            required_default=required_default
        )


    def get_filters(self):
        return super().get_filters() + [
            self.transform_to_tuple,
            partial(self.apply_required_default, default=self.required_default)
        ]

    @staticmethod
    def transform_to_tuple(items):
        for item in items:
            if not isinstance(item, tuple):
                yield None, item
            else:
                yield item

    @staticmethod
    def apply_required_default(items, default):
        for required, args in items:
            if required is None:
                required = default
            yield required, args


class URLBuilder(OptionalPartList):
    def get_filters(self):
        return super().get_filters() + [
            self.filter_empty_items,
            partial(
                self.add_first_item_required_flag,
            ),
            partial(
                self.flatten,
                get_separator=self.get_separator
            ),
            self.join,
        ]

    @staticmethod
    def filter_empty_items(items):
            for required, item in items:
                if item:
                    yield required, item

    @staticmethod
    def add_first_item_required_flag(items):
        try:
            required, item = next(items)
        except StopIteration:
            return False, items
        else:
            return required, chain(
                ((required, item),),
                items
            )

    @staticmethod
    @pass_tuple(1)
    def flatten(items, get_separator):
        required, item = next(items)
        if item:
            yield item
        for required, item in items:
            if item:
                yield get_separator(required)
                yield item

    @staticmethod
    @pass_tuple(1)
    def join(items):
        return ''.join(items)
