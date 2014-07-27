from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from django_crucrudile.routes import ModelViewRoute


class ModelMixin:
    """ModelRouter with no views. Give :attr:`model` kwarg where needed,
    ask it in :func:`__init__`, and map ``SingleObjectMixin`` and
    ``MultipleObjectMixin`` to
    :class:`django_crucrudile.routes.ModelViewRoute` in register
    functions.

    .. inheritance-diagram:: ModelMixin

    """
    model = None
    """
    :attribute model: Model used when building router URL name and URL
                      part, and passed to registered routes. Must be
                      defined at class-level or passed to
                      :func:`__init__`.
    :type model: model
    """
    def __init__(self, model=None, url_part=None, **kwargs):
        """Read model (from args or class-level value (:attr:`model`), fail if
        none found.

        :argument model: see :attr:`model`
        :type model: :class:`django.db.Models`

        :raises ValueError: if model not passed an argument and not
                            defined on class

        """
        # we need to set self.model before calling the superclass
        # __init__, because it will call
        # self.get_auto_register_kwargs() which needs self.model
        if model is not None:
            self.model = model
        elif self.model is None:
            raise ValueError(
                "No ``model`` argument provided to __init__"
                ", and no model defined as class attribute (in {})"
                "".format(self)
            )
        if url_part is not None:
            self.url_part = url_part
        else:
            self.url_part = self.model_url_part
        super().__init__(**kwargs)

    @property
    def model_url_part(self):
        """Return the model name to be used when building the URL part

        :returns: URL part from the Django model name
                  (``model._meta.model_name``)
        :rtype: str

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

    def get_register_map_kwargs(self):
        """Add :attr:`model` as kwarg when applying register map

        :returns: Keyword arguments to pass to mapping value, when
                  applying register map (from
                  :func:`get_register_map`) in :func:`register`
        :rtype: dict

        .. seealso::

           For doctests that use this member, see
           :class:`django_crucrudile.routers.model.ModelRouter`

        """
        kwargs = super().get_register_map_kwargs()
        kwargs['model'] = self.model
        return kwargs

    def get_base_store_kwargs(self):
        """Add :attr:`model` so that the route classes in the base store will
        get the model as a kwarg when being instantiated

        :returns: Keyword arguments to pass to mapping value, when
                  applying class register map (from
                  :func:`get_register_class_map`) in
                  :func:`register_class`
        :rtype: dict

        .. seealso::

           For doctests that use this member, see
           :class:`django_crucrudile.routers.model.ModelRouter`

        """
        kwargs = super().get_base_store_kwargs()
        kwargs['model'] = self.model
        return kwargs

    def get_register_map(self):
        """Add :class:`django_crucrudile.routes.ModelViewRoute` mapping for
        ``SingleObjectMixin`` and ``MultipleObjectMixin``.

        This mapping allows registering Django generic views in the
        base, making them register as
        :class:`django_crucrudile.routes.ModelViewRoute` and
        instantiate with :attr:`model`.

        :returns: Entity store mappings
        :rtype: dict

        .. seealso::

           For doctests that use this member, see
           :class:`django_crucrudile.routers.model.ModelRouter`

        """
        mapping = super().get_register_map()
        mapping.update({
            (SingleObjectMixin, MultipleObjectMixin):
            ModelViewRoute,
        })
        return mapping

    @classmethod
    def get_register_class_map(cls):
        """Add :func:`django_crucrudile.routes.ModelViewRoute.make_for_view`
        mapping for ``SingleObjectMixin`` and ``MultipleObjectMixin``.

        This mapping allows registering Django generic views in the
        base store, so that entities made using
        :class:`django_crucrudile.routes.ModelViewRoute` (and
        instantiated with :attr:`model`) get registered in the entity
        store when :class:`ModelMixin` gets instantiated (in
        :func:`django_crucrudile.entities.store.EntityStore.register_base_store`).

        :func:`django_crucrudile.routes.ModelViewRoute.make_for_view`
        creates a new :class:`django_crucrudile.routes.ModelViewRoute`
        class, and uses its argument as the
        :attr:`django_crucrudile.routes.ViewRoute.view_class` attribute.

        :returns: Base store mappings
        :rtype: dict

        .. seealso::

           For doctests that use this member, see
           :class:`django_crucrudile.routers.model.ModelRouter`

        """
        mapping = super().get_register_class_map()
        mapping.update({
            (SingleObjectMixin, MultipleObjectMixin):
            ModelViewRoute.make_for_view
        })
        return mapping
