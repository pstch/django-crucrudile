Routes and route mixins
=======================

.. contents::

.. module:: django_crucrudile.routes

A route is an implementation of the
:class:`django_crucrudile.entities.Entity` abstract class that yields
URL patterns made from its attributes. In the code, this is
represented by subclassing :class:`django_crucrudile.entities.Entity`
and providing a generator in ``patterns()``, yielding URL patterns
made from the route attributes. When route classes provide
:func:`django_crucrudile.entities.Entity.patterns`, it makes them
become concrete implementations of the Entity abstract class. Route
classes themselves are abstract by nature and need a definition of the
abstract function :func:`base.BaseRoute.get_callback`.


- :class:`CallbackRoute` : Implements :class:`base.BaseRoute` using
  :class:`mixins.callback.CallbackMixin` that provides an
  implementation of :func:`base.BaseRoute.get_callback` that returns
  the callback set on the route (either in
  :func:`CallbackRoute.__init__` or as class attribute)
- :class:`ViewRoute` : Implements :class:`base.BaseRoute` using
  :class:`mixins.view.ViewMixin` that provides an implementation of
  :func:`base.BaseRoute.get_callback` that returns the a callback
  obtaining from the view class set on the route (either in
  :func:`mixins.view.ViewMixin.__init__` or as class attribute).
- :class:`ModelViewRoute` : Implements :class:`base.BaseRoute` using
  :class:`mixins.view.ViewMixin` and :class:`mixins.model.ModelMixin`,
  passes the model in the view keyword arguments, and can be used with
  Django generic views.

.. note ::

  :class:`ModelViewRoute` Can also be used in a
  :class:`django_crucrudile.routers.model.ModelRouter` store register
  mapping, as it correctly uses the model given in
  :class:`django_crucrudile.routers.mixins.model.ModelMixin.get_register_map_kwargs`
  and
  :class:`django_crucrudile.routers.mixins.model.ModelMixin.get_base_store_kwargs`,
  and the view class that can then be registered in the resulting
  router.

Base route
----------

.. automodule:: django_crucrudile.routes.base
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__

Route mixins
------------

.. automodule:: django_crucrudile.routes.mixins
   :no-members:

Abstract
>>>>>>>>

Arguments
~~~~~~~~~

.. automodule:: django_crucrudile.routes.mixins.arguments
   :no-members:

.. autoclass:: django_crucrudile.routes.mixins.arguments.ArgumentsMixin
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__

Parser
++++++

.. automodule:: django_crucrudile.routes.mixins.arguments.parser
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__


Model
~~~~~

.. automodule:: django_crucrudile.routes.mixins.model
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__


Concrete
>>>>>>>>

Callback
~~~~~~~~

.. automodule:: django_crucrudile.routes.mixins.callback
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__


View
~~~~

.. automodule:: django_crucrudile.routes.mixins.view
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__



.. module:: django_crucrudile.routes
   :noindex:

Callback route
--------------

.. autoclass:: django_crucrudile.routes.CallbackRoute
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__

View route
----------

.. autoclass:: django_crucrudile.routes.ViewRoute
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__

Model view route
----------------

.. autoclass:: django_crucrudile.routes.ModelViewRoute
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__
