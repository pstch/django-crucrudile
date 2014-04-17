"""
Utility functions
=================

This module contains four utility functions, used by other
``django-crucrudile`` modules. They are pretty simple, which is why
they're just tossed in here, and not in their own modules.`

This module is imported by ``views.mixins`` (for :func:`try_calling`
and :func:`monkeypatch_mixin`)and ``models.mixins`` (for
:func:`convert_camel_case`). Should it become any longer, it may be
wise to split it.

----------------

"""
import re


def try_calling(arg, *args, **kwargs):
    """Evaluate and return arg (with given args and kwargs) if it's a
    callable, otherwise return None

    """
    return arg(*args, **kwargs) if callable(arg) else None


def convert_camel_case(camel_cased, separator):
    """Convert camel cased into words separated by the given separator

    :param camel_cased: Camel cased input string (ex: ``"CamelCased"``)
    :type camel_cased: str
    :param separator: Separator to use (ex: ``"-"``)
    :type separator: str

    :return: converted text (ex: ``"camel-cased"``)
    :rtype: str

    """
    separator_expression = r'\1%s\2' % separator
    step = re.sub('(.)([A-Z][a-z]+)',
                  separator_expression,
                  camel_cased)
    return re.sub('([a-z0-9])([A-Z])',
                  separator_expression,
                  step).lower()


def _is_special_attribute(attr):
    """Return True if attr is the name of a Python special attribute,
    otherwise False

    :param attr: Name of attribute to test
    :type attr: str

    :return: True if attr is special attribute, otherwise False
    :rtype bool:

    """
    return \
        attr.startswith('__') and \
        attr.endswith('__')


def monkeypatch_mixin(class_, mixin):
    r"""Monkeypatch all non-special (bound and unbound) attributes of
    ``mixin`` into ``class_``, then return ``class_``.

    :param class\_: Class to monkeypatch
    :type class\_: class

    :param mixin: Mixin to inject in ``class_``
    :type mixin: class

    :return: Monkeypatched ``class_``
    :rtype: class

    """
    for attr in dir(mixin):
        if not _is_special_attribute(attr) and \
           not hasattr(class_, attr):
            # we found a non-special attribute in ModeActionMixin
            # that is not present in view_class
            # let's monkeypatch it to class_
            setattr(
                class_,
                attr,
                mixin.__dict__[attr]
            )
            # we use .__dict__[] because we need unbound
            # attributes
    return class_
