from django.db.models import Model
from django.views.generic import View

from django_crucrudile.routes import (
    ViewRoute,
    ListRoute,
    DetailRoute,
    CreateRoute,
    UpdateRoute,
    DeleteRoute
)

from .base import (
    BaseRouter, BaseModelRouter,
    provides
)

__all__ = ["Router", "ModelRouter", "provides"]


class Router(BaseRouter):
    """RoutedEntity that yields an URL group containing URL patterns from
    the entities in the entity store. The URL group can be set have an URL
    part and a namespace.

    .. inheritance-diagram:: Router
    """
    @property
    def register_map(self):
        return {
            Model: ModelRouter,
            View: ViewRoute,
        }


@provides(ListRoute)
@provides(DetailRoute)
@provides(CreateRoute)
@provides(UpdateRoute)
@provides(DeleteRoute)
class ModelRouter(BaseModelRouter, Router):
    """
    .. inheritance-diagram:: ModelRouter
    """
    pass
