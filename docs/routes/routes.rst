Routes and route mixins
=======================

.. contents::

.. module:: django_crucrudile.routes

.. automodule:: django_crucrudile.routes
   :no-members:
   :noindex:

.. testsetup::

   from mock import Mock

   from django_crucrudile.routes.base import BaseRoute
   from django_crucrudile.routes import (
       ArgumentsMixin, CallbackMixin, ViewMixin, ModelMixin
   )
   from django_crucrudile.routes.mixins.arguments.parser import (
       combine, ArgumentsParser
   )


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



Route implementations
---------------------

.. automodule:: django_crucrudile.routes
   :noindex:
