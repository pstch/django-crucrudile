Getting started
===============

.. contents::

.. warning:: TODO

Introduction
------------

Abstract
~~~~~~~~

This package can be used to simplify Django's URL pattern definitions. It's able to generate a Django URL pattern structure from a directed acylic graph represented using :

 - Routes (leaves in the graph), contain URL patterns
 - Routers (nodes in the graph), contain routes

Example :

.. graphviz::

   digraph intro_ex {
       size="4, 2"
       bgcolor="transparent"
       edge[fontsize=10]
       node[fontsize=12]

       "Router" -> "Route : home page"
       "Router" -> "Route : application status"

   }

A router can also contain other routers :

.. graphviz::

   digraph intro_ex_2 {
       size="6, 3"
       bgcolor="transparent"
       edge[fontsize=10]
       node[fontsize=12]

       "Router" -> "Route : home page"
       "Router" -> "Route : application status"

       "Router" -> "Router : help"
       "Router : help" -> "Route : getting help"
       "Router : help" -> "Route : version"

   }

This allows us to define complex routing graphs using combinations of route and router objects. The route and router objects handle :

 - URL namespaces (in routers)
 - URL regex building (with multiple parts, routers can also prefix the routes they contain using their own URL regex part)
 - building a Django URL pattern tree

.. warning::

   The routing graph must be **acyclic** as we parse it recursively,
   using a depth-first search. (django-crucrudile does not (yet ?)
   support infinite routing graphs)

Routes and router
~~~~~~~~~~~~~~~~~

Here, we defined a routing graph, but we never actually defined what to point our routes to. In fact, the above structure could not be created in django-crucrudile, because a route is an abstract object (Python abstract class) that doesn't know what callback to use in its generated patterns.

As the route is an abstract object, we use "implementations" of this object (they know what callback to use in the generated patterns, they are "concrete"). django-crucrudile provides two basic implementations of the route class :
p
 - Callback route : a simple route that uses a given callback
 - View route : a route that uses a callback from a given Django view class.

If we take that previous example, using view routes in lieu of routes, we get :

.. graphviz::

   digraph intro_ex_2 {
       size="6, 3"
       bgcolor="transparent"
       edge[fontsize=10]
       node[fontsize=12]

       "Router" -> "View route : home page"
       "Router" -> "View route : application status"

       "Router" -> "Router : help"
       "Router : help" -> "View route : getting help"
       "Router : help" -> "View route : version"

   }

.. note:: The view route leaves in this example are **instances of the view route class**. They need a view_class to get instantiated. The route names (that will be used to build the URL regex as well as the URL name) should also be passed to the constructor (otherwise the route name will be built from the view class name, stripping of the tailing "View" if needed).

.. note::  The router nodes in this example are **instances of the router class**. They don't need anything to get instantantiated, but they can take a router name (used to build the router URL part) and a router namespace (used to wrap routers in Django URL namespaces).

Here is the code corresponding to that example :

.. automodule:: tests.doctests.examples.quickstart.intro_ex

As you can see, we can pass the URL part to the help router, to prefix the resulting URL patterns. Here are the URLs corresponding to that example :

.. graphviz::

   digraph intro_ex_urls {
       size="6, 3"
       bgcolor="transparent"
       edge[fontsize=10]
       node[fontsize=12]

       "/" -> "/home"
       "/" -> "/status"

       "/" -> "/help/"

       "/help/" -> "/help/help"
       "/help/" -> "/help/version"

   }

The generator returned the ``patterns()`` function of the router yields URL objects that can be used in the ``url_patterns`` attribute of ``urls.py``.

Index URLs and redirections
---------------------------

The base route and router objects support setting an object as "index", which means that when it is added to a router, the router set it as its redirect target.

In the previous example, if the home route was as index, requests to ``/`` would get redirected to ``/home``.

To achieve this, a route is added in each router that has a rediect. This route is a view route that uses a Django generic redirection view that points to the redirect target. If the redirect target is itself a router, we use this router's redirect target, and so on, until we find a route.

To mark a route or router as "index", set its ``index`` attribute to ``True``. You can also add it as index, using the ``index`` argument of the register method : that won't alter the ``index`` attribute, but will still add as index.

Here is what the previous example would look like, with a redirection from ``/`` to "/home" and from "/help/" to "/help/help" :

.. automodule:: tests.doctests.examples.quickstart.intro_ex_redir

.. graphviz::

   digraph intro_ex_urls_redirs {
       size="6, 3"
       bgcolor="transparent"
       edge[fontsize=10]
       node[fontsize=12]

       "/" -> "/home"
       "/" -> "/status"

       "/" -> "/help/"

       "/help/" -> "/help/help"
       "/help/" -> "/help/version"

       subgraph redirects {
           edge[color=blue, label="redirects to"]
           "/" -> "/home"
           "/help/" -> "/help/help"
       }

   }

Using with models
-----------------

.. warning:: TODO

More examples
-------------

Bookstore example
~~~~~~~~~~~~~~~~~

.. automodule:: tests.doctests.examples.bookstore
