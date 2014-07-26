Routers (``Router``, ``BaseModelRouter`` and ``ModelRouter``) [TODO]
====================================================================

.. contents::

.. module:: django_crucrudile.routers

.. automodule:: django_crucrudile.routers
   :noindex:

Base router
-----------

.. autoclass:: Router
   :members:
   :undoc-members:
   :show-inheritance:

Model router
------------

.. autoclass:: BaseModelRouter
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: ModelRouter
   :members:
   :undoc-members:
   :show-inheritance:

The following graph may help to explain the relation between the
generic views, routes and routers :

.. graphviz::

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
