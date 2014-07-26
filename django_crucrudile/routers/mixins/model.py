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
    def get_register_map_kwargs(self):
        """Give :attr:`model` as kwarg when applying register map. """
        kwargs = super().get_register_map_kwargs()
        kwargs['model'] = self.model
        return kwargs

    def get_base_store_kwargs(self):
        """Add :attr:`model` to upstream auto register kwargs, so that the
        route classes in the base store will get the model as a kwarg when
        being instantiated.

        """
        kwargs = super().get_base_store_kwargs()
        kwargs['model'] = self.model
        return kwargs

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
        """Return the model name to be used when building the URL part"""
        return self.model._meta.model_name

    def get_register_map(self):
        """Override to append mapping of ``SingleObjectMixin`` and
        ``MultipleObjectMixin`` to
        :class:`django_crucrudile.routes.ModelViewRoute`.

        """
        mapping = super().get_register_map()
        mapping.update({
            (SingleObjectMixin, MultipleObjectMixin):
            ModelViewRoute,
        })
        return mapping

    @classmethod
    def get_register_class_map(cls):
        """Override to append mapping of ``SingleObjectMixin`` and
        ``MultipleObjectMixin`` to
        :func:`django_crucrudile.routes.ModelViewRoute.make_for_view`
        .

        We use
        :func:`django_crucrudile.routes.ModelViewRoute.make_for_view`
        because we are here registering the class map (base store),
        whose values are themselves classes (Entity classes), that
        will be called the get the registered entity instance.

        :func:`django_crucrudile.routes.ModelViewRoute.make_for_view`
        creates a new :class:`django_crucrudile.routes.ModelViewRoute`
        class, and uses its argument as the
        :attr:`django_crucrudile.routes.ViewRoute.view_class` class
        attribute.

        (if we returned directly a
        :class:`django_crucrudile.routes.ModelViewRoute` in the
        mapping, the registered entity "class" would be an entity
        **instance**).

        """
        mapping = super().get_register_class_map()
        mapping.update({
            (SingleObjectMixin, MultipleObjectMixin):
            ModelViewRoute.make_for_view
        })
        return mapping
