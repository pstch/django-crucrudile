django-crucrudile
=================

.. module:: django_crucrudile

.. toctree::
   installation
   quickstart
   entities/entity_store
   entities/entities
   routers/routers
   urlutils
   routes/routes
   tests
   examples/bookstore

* :ref:`modindex`
* :ref:`genindex`

.. automodule:: django_crucrudile
   :noindex:

Class structure graph
---------------------

.. graphviz::

   digraph class_structure {

     bgcolor="transparent"

     "Abstract" [color=black, fontcolor=white, style=filled]
     "Concrete"

     "Entity" [color=black, fontcolor=white, style=filled]
     "BaseRoute" [color=black, fontcolor=white, style=filled]

     "Entity" -> "BaseRoute"
     "Entity" -> "Router"
     "EntityStore" -> "Router"

     "Router" -> "BaseModelRouter"
     "BaseModelRouter" -> "ModelRouter"

     "ArgumentsMixin"[color=black, fontcolor=white, style=filled]
     "ModelMixin"[color=black, fontcolor=white, style=filled]
     "CallbackMixin"
     "ViewMixin"

     "BaseRoute" -> "CallbackRoute"
     "ArgumentsMixin" -> "CallbackRoute"
     "CallbackMixin" -> "CallbackRoute"

     "BaseRoute" -> "ViewRoute"
     "ArgumentsMixin" -> "ViewRoute"
     "ViewMixin" -> "ViewRoute"

     "BaseRoute" -> "ModelViewRoute"
     "ArgumentsMixin" -> "ModelViewRoute"
     "ViewMixin" -> "ModelViewRoute"
     "ModelMixin" -> "ModelViewRoute"

   }
