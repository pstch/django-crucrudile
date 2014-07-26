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

    .. warning::

       Because this is an abstract class, the **documentation tests**
       use an implementation (``ModelRoute``) of
       :class:`django_crucrudile.routes.base.BaseRoute` and
       :class:`ModelMixin`, with a dummy :func:`get_callback`
       function.

    .. testsetup::

       class ModelRoute(ModelMixin, BaseRoute):
           def get_callback(self): pass

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
                 **kwargs):
        """Initialize ModelRoute, check that model is defined at class-level
        or passed as argument.

        :argument model: See :attr:`model`

        :raises ValueError: ``model`` argument is None, and no model
                            defined in :attr:`model`

        """
        if model is not None:
            self.model = model
        elif self.model is None:
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

        .. testcode::

           model = Mock()
           model._meta.model_name = 'testmodel'
           route = ModelRoute(model=model, name='routename')
           print(route.model_url_name)

        .. testoutput::

           testmodel

        """
        return self.model._meta.model_name


    @property
    def model_url_part(self):
        """Return the model name to be used when building the URL part

        :returns: URL part from the URL name (:func:`model_url_name`)
        :rtype: str

        .. testcode::

           model = Mock()
           model._meta.model_name = 'testmodel'
           route = ModelRoute(model=model, name='routename')
           print(route.model_url_part)

        .. testoutput::

           testmodel

        """
        return self.model._meta.model_name


    def get_url_specs(self):
        """Return URL specs where the model URL name is appended to the prefix
        part list

        .. testcode::

           model = Mock()
           model._meta.model_name = 'testmodel'
           route = ModelRoute(model=model, name='routename')
           print(list(route.get_url_specs()))

        .. testoutput::
           :options: +NORMALIZE_WHITESPACE

           [([], ['routename'], [])]

        With arguments :

        .. testsetup::

           class ArgsModelRoute(ArgumentsMixin, ModelRoute):
               pass

        .. testcode::

           model = Mock()
           model._meta.model_name = 'testmodel'
           route = ArgsModelRoute(
               model=model, name='routename',
               arguments_spec=["<pk>", "<slug>"]
           )
           print(list(route.get_url_specs()))

        .. testoutput::
           :options: +NORMALIZE_WHITESPACE

           [([],
             ['routename'],
             [(True, '<pk>/<slug>')])]

        With :attr:`prefix_url_part` set to ``True`` :

        .. testsetup::

           class PrefixModelRoute(ModelRoute):
               prefix_url_part = True

        .. testcode::

           model = Mock()
           model._meta.model_name = 'testmodel'
           route = PrefixModelRoute(
               model=model, name='routename',
           )
           print(list(route.get_url_specs()))

        .. testoutput::
           :options: +NORMALIZE_WHITESPACE

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

        .. testcode::

           model = Mock()
           model._meta.model_name = 'testmodel'
           route = ModelRoute(
               model=model, name='routename',
           )
           print(route.get_url_name())

        .. testoutput::

           testmodel-routename

        """
        return "{}-{}".format(self.model_url_name, self.name)
