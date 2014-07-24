from copy import copy
from functools import reduce, partial

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


class ParsableList(list):
    def __add__(self, other):
        if not other:
            return self

        new = copy(self)

        if isinstance(other, list):
            new.extend(other)
        else:
            new.append(other)

        return new

    def get_parsers(self):
        return []

    def __call__(self):
        parsers = self.get_parsers()

        if parsers:
            composed_parsers = compose(reversed(parsers))
            # tuple (bool, str or list (str))
            # or str or list (tuple (bool, str or list (str)) or str)
            # ->
            # iterable(str)
            return composed_parsers(self)
        else:
            return items



class OptionalPartList(ParsableList):
    separator = "/"
    opt_separator = "/?"
    required_default = True

    def __init__(self, iterable=None,
                 separator=None,
                 opt_separator=None,
                 required_default=None):
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
        if iterable is None:
            iterable = []

        super().__init__(iterable)


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

    def get_parsers(self):
        return super().get_parsers() + [
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
    _first_item_required = True

    def get_first_item_required(self):
        return self._first_item_required

    def set_first_item_required(self, value):
        self._first_item_required = value

    def get_parsers(self):
        return super().get_parsers() + [
            self.parser_empty_items,
            partial(
                self.flag_first_item_required,
                flag_setter=self.set_first_item_required
            ),
            partial(
                self.flatten,
                get_separator=self.get_separator
            ),
            self.join,
            partial(
                self.add_first_item_required_flag,
                flag_getter=self.get_first_item_required
            )
        ]

    @staticmethod
    def parser_empty_items(items):
            for required, item in items:
                if item:
                    yield required, item

    @staticmethod
    def flag_first_item_required(items, flag_setter):
        required, item = next(items)
        flag_setter(required)
        yield required, item
        for required, item in items:
            yield required, item

    @staticmethod
    def flatten(items, get_separator):
        required, item = next(items)
        if item:
            yield item
        for required, item in items:
            if item:
                yield get_separator(required)
                yield item

    @staticmethod
    def join(items):
        return ''.join(items)

    @staticmethod
    def add_first_item_required_flag(items, flag_getter):
        return flag_getter(), items
