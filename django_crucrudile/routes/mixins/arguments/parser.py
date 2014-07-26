"""This module contains the default arguments parser
(:class:`ArgumentsParser`), used in
:class:`django_crucrudile.routes.mixins.arguments.ArgumentsMixin`.

The :func:`combine` function is used by the cartesian product in
:func:`ArgumentsParser.cartesian_product`, it joins an iterable
(filtering out its items that evaluate to ``None``) using a given
separator.

"""
from functools import partial, reduce
from itertools import product

from django_crucrudile.urlutils import OptionalPartList


def combine(iterable, separator):
    """Join ``iterable`` (filtering out its items that evaluate to
    ``Ǹone``) using ``separator``

    :argument iterable: Iterable to filter and join
    :type iterable: iterable

    :argument separator: Separator to join with
    :type separator: str

    :returns: Joined string
    :rtype: str

    .. testcode::

       print(combine(['Foo', '', 'Bar', None, 'Xyz', 0], '/'))

    .. testoutput::

       Foo/Bar/Xyz

    """
    return separator.join(filter(None, iterable))

class ArgumentsParser(OptionalPartList):
    """This parser reads a list of argument specification, and builds an
    argument combination list (using a cartesian product). It subclasses
    :class:`django_crucrudile.urlutils.OptionalPartList` (as an arguments
    list is an URL part list), and add its building parsers in
    :func:`ArgumentsParser.get_parsers()`.

    The input of the parser should be a list of argument
    specifications. Argument specifications can be written as :

    - ``(bool, string)`` : converted to ``(bool, list([string]))``
    - ``string`` : converted to ``(True, list([string]))``
    - ``list`` : converted to ``(True, list)``

    If ``bool`` is not defined, a default value will be used (see :attr:`django_crucrudile.urlutils.Separated.required_default`).

    In ``(bool, list)`` :

    - ``bool`` is a boolean flag indicating whether an argument list
      is required
    - ``list`` is a list of argument, as "choices" : a
      combination will be generated for each item in the list

    The output of the parser is a list of 2-tuple containing a boolean
    value and a string. The boolean value is a flag indicating whether
    the first argument of the string is required, and the string is
    the joined URL parts of the argument combination.

    To set the separators, see
    :attr:`django_crucrudile.urlutils.Separated.separator` and
    :attr:`django_crucrudile.urlutils.Separated.opt_separator`.

    .. inheritance-diagram:: ArgumentsParser

    Test, with first argument **required** :

    .. testcode ::

       parser = ArgumentsParser([
           ["<arg1.1>", "<arg2.2>"],
           "<arg3>",
           (False, ["<arg4.1>", "<arg4.2>"]),
           (True, ["<args5>"])
       ])
       print(list(parser()))

    .. testoutput ::
       :options: +NORMALIZE_WHITESPACE

       [(True, '<arg1.1>/<arg3>/?<arg4.1>/<args5>'),
        (True, '<arg1.1>/<arg3>/?<arg4.2>/<args5>'),
        (True, '<arg2.2>/<arg3>/?<arg4.1>/<args5>'),
        (True, '<arg2.2>/<arg3>/?<arg4.2>/<args5>')]

    Test, with first argument **not required** :

    .. testcode ::

       parser = ArgumentsParser([
           (False, ["<arg1.1>", "<arg1.2>"]),
           (None, ["<arg3>"]),
           (False, ["<args4>"])
       ])
       print(list(parser()))

    .. testoutput ::
       :options: +NORMALIZE_WHITESPACE

       [(False, '<arg1.1>/<arg3>/?<args4>'),
        (False, '<arg1.2>/<arg3>/?<args4>')]

    """
    def get_parsers(self):
        """Add :func:`transform_args_to_list`, :func:`cartesian_product` and :func:`consume_cartesian_product` to the parsers from :func:`django_crucrudile.urlutils.OptionalPartList.get_parsers`.

        :returns: Argument parsers list
        :rtype: list of callable
        """
        return super().get_parsers() + [
            # iterable(tuple (bool, str or list (str))) ->
            # iterable(tuple (bool, list(str))) ->
            self.transform_args_to_list,
            # iterable(tuple (bool, list(str))) ->
            # iterable(str)
            partial(self.cartesian_product, get_separator=self.get_separator),
            self.consume_cartesian_product
        ]

    @staticmethod
    def transform_args_to_list(items):
        """Transform second part of each item in items in a list if it's not
one.

        :argument items: List of items to transform
        :type items: iterable of 2-tuple

        :returns: Transformed list
        :rtype: iterable of 2-tuple : [(bool, list)]

        .. testcode ::

           print(list(ArgumentsParser.transform_args_to_list([
               (None, '<arg1>'),
               (None, ['<arg2>', '<arg3>'])
           ])))

        .. testoutput ::
           :options: +NORMALIZE_WHITESPACE

           [(None, ['<arg1>']),
            (None, ['<arg2>', '<arg3>'])]

        """
        for required, args in items:
            if not isinstance(args, list):
                args = [args, ]
            yield required, args


    @staticmethod
    def cartesian_product(items, get_separator):
        """Process cartesian product to get all possible combinations with argument lists in ``items``.

        :argument items: List of tuple to transform (2-tuple with a
                         flag indicating if the argument specification
                         is required, and the argument choice list)
        :type items: iterable of 2-tuple

        :returns: List of 2-tuple, with a flag indicating if the first
                  item is required, and the joined list.
        :rtype: iterable of 2-tuple : [(bool, str)]

        With first spec **required** :

        .. testcode ::

           get_separator = lambda x: '/' if x else '/?'

           print(list(ArgumentsParser.cartesian_product([
               (True, ['<arg1>']),
               (True, ['<arg2>', '<arg3>']),
               (False, ['<arg4>', '<arg5>'])
           ], get_separator=get_separator)))

        .. testoutput ::
           :options: +NORMALIZE_WHITESPACE

            [(True, '<arg1>/<arg2>/?<arg4>'),
             (True, '<arg1>/<arg2>/?<arg5>'),
             (True, '<arg1>/<arg3>/?<arg4>'),
             (True, '<arg1>/<arg3>/?<arg5>')]

        With first spec **not required** :

        .. testcode ::

           get_separator = lambda x: '/' if x else '/?'

           print(list(ArgumentsParser.cartesian_product([
               (False, ['<arg1>']),
               (True, ['<arg2>', '<arg3>']),
               (False, ['<arg4>', '<arg5>'])
           ], get_separator=get_separator)))

        .. testoutput ::
           :options: +NORMALIZE_WHITESPACE

            [(False, '<arg1>/<arg2>/?<arg4>'),
             (False, '<arg1>/<arg2>/?<arg5>'),
             (False, '<arg1>/<arg3>/?<arg4>'),
             (False, '<arg1>/<arg3>/?<arg5>')]

        """
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

    @staticmethod
    def consume_cartesian_product(items):
        """Force the generated to be consumed

        :argument items: Generator to consume
        :type items: iterable

        :returns: Consumed list
        :rtype: list

        .. testcode::

           def test_gen():
               yield 1
           print(ArgumentsParser.consume_cartesian_product(test_gen()))

        .. testoutput::

           [1]

        """
        return list(items)
