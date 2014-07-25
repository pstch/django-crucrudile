URL utils
=========

.. module:: django_crucrudile.urlutils

.. automodule:: django_crucrudile.urlutils
   :noindex:

.. testsetup::

   from django_crucrudile.urlutils import *

Decorators
----------

This module defines the :func:`pass_tuple` decorator, that makes a function :
 - run witout the first part of its original arguments
 - return the omitted arguments and its original return value

This allows to use chain of functions in :class:`Parsable` that work only on a slice of the arguments (for example, to run some operations while passing a boolean flag).

.. autofunction:: pass_tuple

Functions
---------

This module defines the :func:`compose` function, that compose a list
of functions into a single function that returns its arguments, passed
in chain to each of the functions. This function is used by
:class:`Parsable` to compose the filters returned by
:func:`Parsable.get_filters`, in :func:`Parsable.__call__`.

.. autofunction:: compose

Classes
-------

 - :class:`Separated` allows
   separator-related options to be passed to :func:`Separated.__init__`
   and provides a :func:`Separated.get_separator`.
 - :class:`Parsable` provides a class which instances can be called
   (:func:`Separated.__call__`), to return the "parsed" version of the
   instance. The parsed version is made by passing the instance through
   the functions returned by :func:`Separated.get_parsers()`.
 - :class:`OptionalPartList` provides a class that implements
   :class:`Separated` and :class:`Parsable` with a :py:class:`list`, and
   that provides two parsers (that, if needed : transform the original
   items in tuples ; set the "required" flag to the default value)
 - :class:`URLBuilder` subclasses :class:`OptionalPartList` and
   provides parsers , on top of the original ones, to join the URL
   parts with adequate separators where required.


Generic
+++++++

.. note::

   These classes provide bases for the :class:`URLBuilder` and
   :class:`django_crucrudile.routes.arguments.parser.ArgumentsParser`
   classes.

.. autoclass:: Separated
   :members:
   :undoc-members:
   :special-members:
   :exclude-members: __dict__, __module__, __weakref__
   :show-inheritance:

.. autoclass:: Parsable
   :members:
   :undoc-members:
   :special-members:
   :exclude-members: __dict__, __module__, __weakref__
   :show-inheritance:

URL parts classes
+++++++++++++++++

Optional URL parts list
~~~~~~~~~~~~~~~~~~~~~~~

.. graphviz::

   digraph opt_part_list_parsers {
       bgcolor="transparent"
       edge[fontsize=10, weight=1.2]
       node[fontsize=12, nodesep=0.75, ranksep=0.75]

       subgraph t_t_t {
           rank="same"
           rankdir="LR"
           "..."[style="filled", fillcolor="#BBFFBB", color="green"]
           "[(required, ...)]"[style="filled", fillcolor="#BBFFBB", color="green"]
           "transform_to_tuple"[style="filled", fillcolor="#BBBBFF", color="blue"]
       }

       subgraph a_r_d {
           rank="same"
           rankdir="LR"
           "[(None, ...)]"
           "[(bool, ...)]"
           "apply_required_default"[style="filled", fillcolor="#BBBBFF", color="blue"]
       }

       "[(required, ...)]" -> "transform_to_tuple"
       "..." -> "transform_to_tuple"
       "transform_to_tuple" -> "[(required, ...)] "

       "[(required, ...)] " -> "[(None, ...)]"
       "[(required, ...)] " -> "[(bool, ...)]"

       "[(None, ...)]" -> "apply_required_default"
       "[(bool, ...)]" -> "apply_required_default"
       "apply_required_default" -> "[(bool, ...)] "

       subgraph types {
           node[style=filled, color="#eeeeee",
                fontcolor="#555555", fontsize=10]

           "[(required, ...)]"
           "..."
           "[(required, ...)] "[style="filled", fillcolor="#FFFFBB"]
           "[(None, ...)]"[style="filled", fillcolor="#FFFFBB"]
           "[(bool, ...)]"[style="filled", fillcolor="#FFFFBB"]
           "[(bool, ...)] "[style="filled", fillcolor="#FFBBBB", color="red"]
       }

       subgraph io {
          rank="other"
          rankdir="TB"
          node[style="filled"]
          edge[style="invis"]
          "Input"[fillcolor="#BBFFBB", color="green"]
          "Output"[fillcolor="#FFBBBB", color="red"]
          "Intermediate\n values"[fillcolor="#FFFFBB"]
          "Parser"[fillcolor="#BBBBFF", color="blue"]

          "Input" -> "Parser" -> "Intermediate\n values" -> "Output"
       }

   }

.. autoclass:: OptionalPartList
   :members:
   :undoc-members:
   :special-members:
   :exclude-members: __dict__, __module__, __weakref__
   :show-inheritance:

URL Builder
~~~~~~~~~~~~~~~~~~~~~~~

.. graphviz::

   digraph url_builder_parsers {
       bgcolor="transparent"
       edge[fontsize=10, weight=1.2]
       node[fontsize=12, nodesep=0.75, ranksep=0.75]
       subgraph t_t_t {
           rank="same"
           rankdir="LR"
           "..."[style="filled", fillcolor="#BBFFBB", color="green"]
           "[(required, ...)]"[style="filled", fillcolor="#BBFFBB", color="green"]
           "transform_to_tuple"[style="filled", fillcolor="#BBBBFF", color="blue"]
       }

       subgraph a_r_d {
           rank="same"
           rankdir="LR"
           "[(None, ...)]"[style="filled", fillcolor="#FFFFBB"]
           "[(bool, ...)]"[style="filled", fillcolor="#FFFFBB"]
           "apply_required_default"[style="filled", fillcolor="#BBBBFF", color="blue"]
       }

       subgraph f_e_i {
           rank="same"
           rankdir="LR"
           "[(required, None)]"[style="filled", fillcolor="#FFFFBB"]
           "[(required, not None)]"[style="filled", fillcolor="#FFFFBB"]
           "filter_empty_items"[style="filled", fillcolor="#BBBBFF", color="blue"]
       }

       subgraph a_firf {
           rank="same"
           rankdir="LR"
           "add_first_item_required_flag"[style="filled", fillcolor="#BBBBFF", color="blue"]
           "[(required, not None)] "[style="filled", fillcolor="#FFFFBB"]
       }

       subgraph flatten {
           rank="same"
           rankdir="RL"
           "flatten"[style="filled", fillcolor="#BBBBFF", color="blue"]
           "(bool, [(required, not None)])"[style="filled", fillcolor="#FFFFBB"]
       }

       subgraph join {
           rank="same"
           rankdir="RL"
           "join"[style="filled", fillcolor="#BBBBFF", color="blue"]
           "(bool, [str])"[style="filled", fillcolor="#FFFFBB"]
       }

       "[(required, ...)]" -> "transform_to_tuple"
       "..." -> "transform_to_tuple"
       "transform_to_tuple" -> "[(required, ...)] "

       "[(required, ...)] " -> "[(None, ...)]"
       "[(required, ...)] " -> "[(bool, ...)]"

       "[(None, ...)]" -> "apply_required_default"
       "[(bool, ...)]" -> "apply_required_default"
       "apply_required_default" -> "[(bool, ...)] "

       "[(bool, ...)] " -> "[(required, None)]"
       "[(bool, ...)] " -> "[(required, not None)]"

       "[(required, None)]" -> "filter_empty_items"
       "[(required, not None)]" -> "filter_empty_items"

       "filter_empty_items" -> "[(required, not None)] "

       subgraph add_first_item_required_flag {
           edge[dir="back"]
           "add_first_item_required_flag" -> "[(required, not None)] "
       }

       "add_first_item_required_flag" -> "(bool, [(required, not None)])"

       "(bool, [(required, not None)])" -> "flatten"

       "flatten" -> "(bool, [str])"

       subgraph join {
           edge[dir="back"]
           "join" -> "(bool, [str])"
       }

       "join" -> "(bool, str)"

       subgraph types {
           node[style=filled, color="#eeeeee",
                fontcolor="#555555", fontsize=10]

           "[(required, ...)]"
           "..."
           "[(required, ...)] "[style="filled", fillcolor="#FFFFBB"]
           "[(None, ...)]"[style="filled", fillcolor="#FFFFBB"]
           "[(bool, ...)]"[style="filled", fillcolor="#FFFFBB"]
           "[(bool, ...)] "[style="filled", fillcolor="#FFFFBB"]
       }

       "(bool, str)"[style="filled", fillcolor="#BBFFBB", color="green"]

       subgraph io {
           rank="other"
           rankdir="TB"
           node[style="filled"]
           edge[style="invis"]
           "Input"[fillcolor="#BBFFBB", color="green"]
           "Output"[fillcolor="#FFBBBB", color="red"]
           "Intermediate\n values"[fillcolor="#FFFFBB"]
           "Parser"[fillcolor="#BBBBFF", color="blue"]
           "Input" -> "Parser" -> "Intermediate\n values" -> "Output"
       }
   }

.. autoclass:: URLBuilder
   :members:
   :undoc-members:
   :special-members:
   :exclude-members: __dict__, __module__, __weakref__
   :show-inheritance:
