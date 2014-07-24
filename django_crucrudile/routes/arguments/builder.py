from abc import ABCMeta, abstractmethod
from functools import partial, reduce
from itertools import product

from django_crucrudile.urlutils import URLPartList


def combine(iterable, separator):
    return separator.join(filter(None, iterable))


class ArgsBuilder(URLPartList):
    _required = None

    def get_required(self):
        return self._required

    def set_required(self, value):
        self._required = value

    def __init__(self, iterable, *args, **kwargs):
        super().__init__(
            self.apply_filters(iterable),
            *args, **kwargs
        )

    def get_filters(self):
        return super().get_filters() + [
            # iterable(tuple (bool, str or list (str))) -> idem
            partial(self.flag_required, flag_setter=self.set_required),
            # iterable(tuple (bool, str or list (str))) ->
            # iterable(tuple (bool, list(str))) ->
            self.transform_args_to_list,
            # iterable(tuple (bool, list(str))) ->
            # iterable(str)
            partial(self.cartesian_product, get_separator=self.get_separator)
        ]


    @staticmethod
    def flag_required(items, flag_setter):
        items = list(items)
        flag_setter(False)
        for required, args in items:
            if required:
                flag_setter(True)
            yield required, args

    @staticmethod
    def transform_args_to_list(items):
        for required, args in items:
            if not isinstance(args, list):
                args = [args, ]
            yield required, args


    @staticmethod
    def cartesian_product(items, get_separator):
        combs = [None]
        first_item_required = None

        for required, args in items:
            if first_item_required is None:
                first_item_required = required

            separator = get_separator(required)
            _combine = partial(combine, separator=separator)

            combs = map(
                _combine,
                product(combs, args)
            )

        for comb in combs:
            yield first_item_required, comb
