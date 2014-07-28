"""This module contains :class:`ModelMixin`, a route mixin that can be used
to bind a model to a route, and use it when computing route metadata.

"""


class ModelMixin:
    """Route mixin that requires a model to be set either on the class
    (:attr:`model` attribute), or to be passed in :func:`__init__`,
    and provides the URL name and URL part using the model metadata.

    .. warning::

       This mixin does not make
       :class:`django_crucrudile.routes.base.BaseRoute` a concrete
       class !

    .. inheritance-diagram:: ModelMixin

    """
    model = None
    """
    :attribute model: Model to use on the Route
    :type model: :class:`django.db.models.Model`
    """
    prefix_url_part = False
    """
    :attribute prefix_url_part: Prefix the URL part with the model
                                (ex: ``/model/<url_part>``)
    :type prefix_url_part: bool
    """
    def __init__(self,
                 *args,
                 model=None,
                 prefix_url_part=None,
                 **kwargs):
        """Initialize ModelRoute, check that model is defined at class-level
        or passed as argument.

        :argument model: See :attr:`model`
        :argument prefix_url_part: See :attr:`prefix_url_part`

        :raises ValueError: ``model`` argument is None, and no model
                            defined in :attr:`model`

        """
        if model is not None:
            self.model = model
        if prefix_url_part is not None:
            self.prefix_url_part = prefix_url_part
        elif self.model is None:  # pragma: no cover
            raise ValueError(
                "No ``model`` argument provided to __init__"
                ", and no model defined as class attribute (in {})"
                "".format(self)
            )
        super().__init__(*args, **kwargs)

    @property
    def model_url_name(self):
        """Return the model name to be used when building the URL name

        :returns: URL name from model name, using Django internals
        :rtype: str

        >>> from django_crucrudile.routes.base import BaseRoute
        >>> from mock import Mock
        >>>
        >>> class ModelRoute(ModelMixin, BaseRoute):
        ...   def get_callback(self):
        ...     pass
        >>>
        >>> model = Mock()
        >>> model._meta.model_name = 'testmodel'
        >>> route = ModelRoute(model=model, name='routename')
        >>>
        >>> route.model_url_name
        'testmodel'

        """
        return self.model._meta.model_name

    @property
    def model_url_part(self):
        """Return the model name to be used when building the URL part

        :returns: URL part from the URL name (:func:`model_url_name`)
        :rtype: str

        >>> from django_crucrudile.routes.base import BaseRoute
        >>> from mock import Mock
        >>>
        >>> model = Mock()
        >>> model._meta.model_name = 'testmodel'
        >>> route = ModelMixin(model=model)
        >>>
        >>> route.model_url_part
        'testmodel'

        """
        return self.model._meta.model_name

    def get_url_specs(self):
        """Return URL specs where the model URL name is appended to the prefix
        part list if needed

        :returns: URL specifications
        :rtype: iterable of 3-tuple

        >>> from django_crucrudile.routes.base import BaseRoute
        >>> from mock import Mock
        >>>
        >>> class ModelRoute(ModelMixin, BaseRoute):
        ...   def get_callback(self):
        ...     pass
        >>>
        >>> model = Mock()
        >>> model._meta.model_name = 'testmodel'
        >>> route = ModelRoute(model=model, name='routename')
        >>>
        >>> list(route.get_url_specs())
        [([], ['routename'], [])]

        With :attr:`prefix_url_part` set to ``True`` :

        >>> from django_crucrudile.routes.base import BaseRoute
        >>> from mock import Mock
        >>>
        >>> class PrefixModelRoute(ModelMixin, BaseRoute):
        ...   def get_callback(self):
        ...     pass
        ...   prefix_url_part = True
        >>>
        >>> model = Mock()
        >>> model._meta.model_name = 'testmodel'
        >>> route = PrefixModelRoute(
        ...     model=model, name='routename',
        ... )
        >>>
        >>> list(route.get_url_specs())
        ... # doctest: +NORMALIZE_WHITESPACE
        [(['testmodel'],
          ['routename'],
          [])]

        """
        for prefix, name, suffix in super().get_url_specs():
            if self.prefix_url_part:
                yield prefix + [self.model_url_part], name, suffix
            else:
                yield prefix, name, suffix

    def get_url_name(self):
        """Return the URL name built :func:`model_url_name` and
        :attr:`Route.name`.

        :returns: compiled URL name
        :rtype: str

        >>> from django_crucrudile.routes.base import BaseRoute
        >>> from mock import Mock
        >>>
        >>> class ModelRoute(ModelMixin, BaseRoute):
        ...   def get_callback(self):
        ...     pass
        >>>
        >>> model = Mock()
        >>> model._meta.model_name = 'testmodel'
        >>> route = ModelRoute(
        ...     model=model, name='routename',
        ... )
        >>>
        >>> route.get_url_name()
        'testmodel-routename'

        """
        return "{}-{}".format(self.model_url_name, self.name)
