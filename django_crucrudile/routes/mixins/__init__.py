"""
This module contains route mixins, that implement specific functionality for abstract class :func:`django_crucrudile.routes.base.BaseRoute` subclasses. Some of these mixins make the class "concrete" (as the abstract function :func:`django_crucrudile.routes.base.BaseRoute.get_callback` is implemented, the class can be instantiated).
"""

from .arguments import ArgumentsMixin
from .callback import CallbackMixin
from .view import ViewMixin
from .model import ModelMixin


__all__ = [
    "ArgumentsMixin", "CallbackMixin",
    "ViewMixin", "ModelMixin"
]
