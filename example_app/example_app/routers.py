from django.db.models import Model

from django_crucrudile.entities.store import provides
from django_crucrudile.routers import (
    Router, BaseModelRouter
)

from .views import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from .models import (
    Document,
    Group,
    Phase,
    Entity,
    Interface,
    Comment,
    Task
)


class BaseRouter(Router):
    def get_register_map(self):
        mapping = super().get_register_map()
        mapping[Model] = ModelRouter
        return mapping


class DocumentsRouter(BaseRouter):
    namespace = "documents"
    url_part = "documents"


class EntitiesRouter(BaseRouter):
    namespace = "entities"
    url_part = "entities"


@provides(ListView, map_kwargs={'index': True})
@provides(DetailView)
@provides(CreateView)
@provides(UpdateView)
@provides(DeleteView)
class ModelRouter(BaseModelRouter):
    pass


base_router = Router()
documents_router = DocumentsRouter()
entities_router = EntitiesRouter()

documents_router.register(Document, index=True)
documents_router.register(Group)
documents_router.register(Phase)
base_router.register(documents_router, index=True)

entities_router.register(Entity, index=True)
entities_router.register(Interface)
base_router.register(entities_router)

base_router.register(Comment)
base_router.register(Task)
