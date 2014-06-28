from django_crucrudile.routers import (
    Router,
)

from .models import (
    DocumentModel,
    GroupModel,
    PhaseModel,
    EntityModel,
    InterfaceModel,
    CommentModel,
    TaskModel
)


class BaseRouter(Router):
    pass


class DocumentsRouter(BaseRouter):
    namespace = "documents"
    url_part = "documents"


class EntitiesRouter(BaseRouter):
    namespace = "entities"
    url_part = "entities"


base_router = Router()
documents_router = DocumentsRouter()
entities_router = EntitiesRouter()

documents_router.register(DocumentModel, index=True)
documents_router.register(GroupModel)
documents_router.register(PhaseModel)
base_router.register(documents_router, index=True)

entities_router.register(EntityModel, index=True)
entities_router.register(InterfaceModel)
base_router.register(entities_router)

base_router.register(CommentModel)
base_router.register(TaskModel)
