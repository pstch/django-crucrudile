Router and router mixins
========================

.. contents::

.. module:: django_crucrudile.routers

.. automodule:: django_crucrudile.routers
   :noindex:
   :no-members:

Base router
+++++++++++

.. autoclass:: Router
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__

Router mixins
+++++++++++++

Model router mixin
------------------

.. automodule:: django_crucrudile.routers.mixins.model
   :no-members:

.. autoclass:: ModelMixin
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__



Model router
+++++++++++++

.. automodule:: django_crucrudile.routers.model
   :no-members:

.. autoclass:: ModelRouter
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__

Generic model router
--------------------

.. automodule:: django_crucrudile.routers.model.generic
   :no-members:

.. autoclass:: GenericModelRouter
   :special-members:
   :exclude-members: __abstractmethods__, __module__,
                     __dict__, __weakref__

The following graph may help to explain the relation between the
generic views, routes and routers :

.. graph2viz::

   digraph model_router {
       bgcolor="transparent"
       edge[dir=back, fontsize=10]
       node[fontsize=12]
        subgraph baseview {
           edge[label="Subclasses", color="#eeeeee",
                fontcolor="#555555", fontsize=7]
           node[style=filled, color="#eeeeee",
                fontcolor="#555555", fontsize=10]
            "Entity" [fontcolor=black, color="#dddddd",
                     fontsize=12]
            "Entity" -> "Router"
            "EntityStore" -> "Router"
           "Router" -> "BaseModelRouter"
           "BaseModelRouter" -> "ModelRouter"
            "Entity" -> "Route"
            "Route" -> "ModelRoute"
           "Route" -> "ViewRoute"
            "ModelRoute" -> "ModelViewRoute"
           "ViewRoute" -> "ModelViewRoute"
            "ModelViewRoute" -> "ListViewRoute"
           "ModelViewRoute" -> "DetailViewRoute"
           "ModelViewRoute" -> "CreateViewRoute"
           "ModelViewRoute" -> "UpdateViewRoute"
           "ModelViewRoute" -> "DeleteViewRoute"
        }
        subgraph routes {
           node[style=filled]
           "ListViewRoute"
           "DetailViewRoute"
           "CreateViewRoute"
           "UpdateViewRoute"
           "DeleteViewRoute"
       }
        subgraph views {
           node[style=dashed, color=gray,
                fontcolor=gray, constraint=false, fontsize=8]
           edge[style=dashed, color=gray,
                fontcolor=gray, label="Callback", fontsize=8]
           "ListView" -> "ListViewRoute"
           "DetailView" -> "DetailViewRoute"
           "CreateView" -> "CreateViewRoute"
           "UpdateView" -> "UpdateViewRoute"
           "DeleteView" -> "DeleteViewRoute"
       }
        subgraph router {
           node[style=filled, color=black, fontcolor=white]
           edge[label="Provides", fontsize=10]
           "ListViewRoute" -> "ModelRouter"
           "DetailViewRoute" -> "ModelRouter"
           "CreateViewRoute" -> "ModelRouter"
           "UpdateViewRoute" -> "ModelRouter"
           "DeleteViewRoute" -> "ModelRouter"
       }
    }
