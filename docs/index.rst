django-crucrudile
=================

.. toctree::
   installation
   getting_started
   entity_store
   entities
   routers
   routes

* :ref:`modindex`

Class structure graph
---------------------

.. graphviz::

   digraph class_structure {

     "Abstract" [color=black, fontcolor=white, style=filled]

     "Entity" [color=black, fontcolor=white, style=filled]
     "Route" [color=black, fontcolor=white, style=filled]
     "ModelRoute" [color=black, fontcolor=white, style=filled]

     "Entity" -> "Route"
     "Entity" -> "Router"
     "EntityStore" -> "Router"

     "Router" -> "BaseModelRouter"
     "BaseModelRouter" -> "ModelRouter"

     "Route" -> "ModelRoute"
     "Route" -> "ViewRoute"

     "ModelRoute" -> "ModelViewRoute"
     "ViewRoute" -> "ModelViewRoute"

   }
