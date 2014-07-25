"""This module contains some utility modules for handling URL
building, and the aspect of handling several parts of the URL, each
separated by different separators, that may be provided or not (thus,
handling separators becomes a bit more complicated).

"""
from pprint import pformat
from copy import copy
from itertools import chain
from functools import reduce, partial, wraps

def pass_tuple(count=1):
    """Returns a decorator that wraps a function to make it run witout the
    first part of a tuple in its original arguments and return the omitted
    arguments contatenated with its original return value.

    :argument count: Number of arguments to omit, default 1.
    :type count: int

    :returns: Decorator
    :rtype: function

    .. warning::

       This function is not the actual decorator, but a function that
       returns that decorator (with the given tuple slice index). If
       you use it as a decorator, you should write ``@pass_tuple()``
       instead of ``@pass_tuple``.

    .. testcode::

       func_1 = lambda x: (42, x)
       func_2 = pass_tuple()(lambda x: x + 2)
       func_3 = pass_tuple()(lambda x: x*2)
       func_4 = lambda x: x[0] + x[1]

       func = compose([func_1, func_2, func_3, func_4])

       print(func(8))

    .. testoutput::

       62

    """

    def decorator(func):
        """Wrap a function to make it run witout the first part of a tuple in
        its original arguments and return the omitted items
        concatenated with its original return value.

        """
        @wraps(func)
        def decorated(args_tuple, *args, **kwargs):
            """Return concatenation of omitted items (``args_tuple[:count]``) and
            result of original function called without omitted items
            (``args_tuple[count:]``).

            """
            return args_tuple[:count] + (
                func(
                    *(tuple(args_tuple[count:]) + tuple(args)),
                    **kwargs
                ),
            )
        return decorated

    return decorator


def compose(functions, *args, **kwargs):
    """Compose functions together

    :argument functions: Functions to compose
    :type functions: list of callables

    :returns: Composed function
    :rtype: function

    .. note::

       This function will pass all other arguments and keyword arguments to the composed functions.

    .. testcode::

       funcs = [lambda x: x*2, lambda x: x+2]
       composed = compose(funcs)
       print(composed(5))

    .. testoutput::

       12

    """

    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    funcs = map(
        partial(partial, *args, **kwargs),
        functions
    )

    def composed(x):
        """Composed function"""
        for func in funcs:
            x = func(x)
        return x

    return composed

class Separated:
    """Accepts separator options in :func:`__init__`, and provide
    :func:`get_separator`, that returns the corresponding separator
    for required and optional parts, based on the separator passed to
    :func:`__init__` (or set at class-level).

    .. inheritance-diagram:: Separated

    """
    separator = "/"
    """
    :attribute separator: Separator to use in front of a required item
    :type separator: str
    """
    opt_separator = "/?"
    """
    :attribute opt_separator: Separator to use in front of an optional item
    :type opt_separator: str
    """
    required_default = True
    """
    :attribute required_default: If True, items required by default
                                (when None)
    :type required_default: bool
    """

    def __init__(self,
                 *args,
                 separator=None,
                 opt_separator=None,
                 required_default=None,
                 **kwargs):
        """Initialize, set separator options

        :argument separator: See :attr:`separator`
        :argument opt_separator: See :attr:`opt_separator`
        :argument required_default: See :attr:`required_default`

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

        :returns: Separator
        :rtype: str
        """
        if required is None:
            required = self.required_default
        if required:
            return self.separator
        else:
            return self.opppt_separator

class Parsable:
    """Class whose instances may be called, to return a "parsed"
    version of the list. The parsed version is obtained by passing the
    original version in the parsers returned by :func:`get_parsers`.

    .. inheritance-diagram:: Parsable
    """
    def get_parsers(self):
        """Return parsers list. Base implementation returns an empty list. To
        add new parsers, override this function and append/prepend the
        functions to use as parsers.

        :returns: List of parser functions
        :rtype: list

        """
        return []

    def __call__(self):
        """Compose the parsers in :func:`get_parsers` using :func:`compose`,
        and use the composed function to get the parsed version from the
        original version.

        :returns: output of parsers

        """
        items = self

        parsers = self.get_parsers()
        composed_parsers = compose(parsers)
        # tuple (bool, str or list (str))
        # or str or list (tuple (bool, str or list (str)) or str)
        # ->
        # iterable(str)
        return composed_parsers(items)


class OptionalPartList(Separated, Parsable, list):
    """Implement Separated and Parsable into a list, to make a separated,
    parsable URL part list, that handles optional parts and that uses
    registered parsers (from :func:`get_parsers`) when the instance is
    called.

    Provide two base parsers, that convert, if needed, original
    items in 2-tuples (:func:`transform_to_tuple`), and provide a
    default value for the first item of the tuple if it's None
    (:func:`apply_required_default`).

    .. inheritance-diagram:: OptionalPartList

    """
    def __add__(self, other):
        """Concatenate with other iterable, creating a new object..

        We override :func:`list.__add__` to return a new
        :class:`OptionalPartList` instance, instead of a list
        instance.

        :argument other: Iterable to concatenate with
        :type other: iterable

        :return: Concatenated object
        :rtype: type(self)

        .. testcode::

           a = OptionalPartList(['foo'])
           b = OptionalPartList(['bar'])

           c = a + b

           assert c is not a
           assert c is not b

           print(type(c).__name__)
           print(c)

        .. testoutput::

           OptionalPartList
           ['foo', 'bar']

        """
        if not other:
            return self

        new = copy(self)
        new.extend(other)
        return new

    def __init__(self, iterable=None,
                 separator=None, opt_separator=None, required_default=None):
        """Initialize, use empty list as iterable if None provided.

        :argument iterable: Raw URL part list
        :type iterable: iterable
        :argument separator: See :func:`Separated.__init__`
        :type separator: str
        :argument opt_separator: See :func:`Separated.__init__`
        :type opt_separator: str
        :argument required_default: See :func:`Separated.__init__`
        :type required_default: bool
        """
        if iterable is None:
            iterable = []

        super().__init__(
            iterable,
            separator=separator,
            opt_separator=opt_separator,
            required_default=required_default
        )


    def get_parsers(self):
        """Complement :class:`OptionalPartList` parsers (from
        :func:`OptionalPartList.get_parsers`) with
        :func:`transform_to_tuple` and :func:`apply_required_default`.

        :returns: List of parser functions
        :rtype: list
        """
        return super().get_parsers() + [
            self.transform_to_tuple,
            partial(self.apply_required_default, default=self.required_default)
        ]

    @staticmethod
    def transform_to_tuple(items):
        """Transform each item to a tuple if it's not one

        :argument items: List of items and tuples
        :type items: iterable

        :returns: List of tuples
        :rtype: generator

        .. testcode::

           output = list(OptionalPartList.transform_to_tuple([
               '<1>',
               (None, '<2>')
           ]))

           print(output)

        .. testoutput::

           [(None, '<1>'), (None, '<2>')]

        """
        for item in items:
            if not isinstance(item, tuple):
                yield None, item
            else:
                yield item

    @staticmethod
    def apply_required_default(items, default):
        """Apply default value to first element of item if it's None.

        :argument items: List of tuples
        :type items: iterable
        :argument default: Value to use if none provided
        :type default: boolean

        :returns: List of tuples, with required default value applied
        :rtype: generator

        .. testcode::

           output = list(
               OptionalPartList.apply_required_default([
                   ('<provided>', '<1>'),
                   (None, '<2>')
               ],
               default='<default>')
           )

           print(output)

        .. testoutput::

           [('<provided>', '<1>'), ('<default>', '<2>')]

        """
        for required, args in items:
            if required is None:
                required = default
            yield required, args


class URLBuilder(OptionalPartList):
    """Allows building URLs from a list of URL parts. The parts can be
    required or optional, this information will be used to determine
    which separator to use.

    We subclass :class:`OptionalPartList`, and add our parsers in
    :func:`get_parsers`, so that they are used when the instance gets
    called :

    - :func:`filter_empty_items`
    - :func:`add_first_item_required_flag`
    - :func:`flatten`
    - :func:`join`

    .. inheritance-diagram:: URLBuilder

    """
    def get_parsers(self):
        """Complement :class:`OptionalPartList` parsers (from
        :func:`OptionalPartList.get_parsers`) with :func:`filter_empty_items`,
        :func:`add_first_item_required_flag`, :func:`flatten` and
        :func:`join`.

        :returns: List of parser functions
        :rtype: list
        """
        return super().get_parsers() + [
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
        """
        Filter out items that give False when casted to boolean.

        :argument items: List of tuples
        :type items: iterable

        :returns: List of URL part specs (with empty items cleared out)
        :rtype: list of tuples

        .. testcode::

           output = URLBuilder.filter_empty_items(
              [(None, ''),
               (None, '<not empty>'),
               (None, []),
               (None, None),
               (None, '<not empty 2>')],
           )

           output = list(output)

           print(output)

        .. testoutput::

           [(None, '<not empty>'), (None, '<not empty 2>')]

        """
        for required, item in items:
            if item:
                yield required, item

    @staticmethod
    def add_first_item_required_flag(items):
        """
        Return a boolean indicating whether the first item is required, and the list of items.

        :argument items: List of tuples
        :type items: iterable

        :returns: Tuple with "first item required" flag, and item list
        :rtype: tuple : (boolean, list)

        .. testcode::

           output = URLBuilder.add_first_item_required_flag(
              [(False, '<opt>'), (True, '<req>')]
           )

           output = output[0], list(output[1])

           print(output)

        .. testoutput::

           (False, [(False, '<opt>'), (True, '<req>')])
        """
        items = iter(items)
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
        """Flatten items, adding the separator where required.

        :argument items: List of tuples
        :type items: iterable

        :returns: List of URL parts with separators
        :rtype: generator

        .. warning::

           This function is decorated using :func:`pass_tuple`, the
           first part of the tuple in its arguments will be omitted,
           and inserted at the beginning of the return value,
           automatically. See the documentation of :func:`pass_tuple`
           for more information.

        .. testcode::

           get_separator = lambda x: '/'

           output = URLBuilder.flatten(
              (
                  None,
                  [(True, '<1>'), (True, '<2>')]
              ), get_separator
           )

           output = output[0], list(output[1])

           print(output)

        .. testoutput::

           (None, ['<1>', '/', '<2>'])

        """
        items = iter(items)
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
        """
        Concatenate items into a string

        :argument items: List of URL parts, with separators
        :type items: list of str

        :returns: Joined URL parts
        :rtype: str

        .. warning::

           This function is decorated using :func:`pass_tuple`, the
           first part of the tuple in its arguments will be passed
           automatically. See the documentation of :func:`pass_tuple`
           for more information.

        .. testcode::

           print(
               URLBuilder.join(
                   (None, ['a', 'b'])
               )
           )

        .. testoutput::

           (None, 'ab')

        """
        return ''.join(items)
