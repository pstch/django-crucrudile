from django_crucrudile.routers import (
    Router,
)

from .models import (
    TestDocumentModel,
    TestGroupModel,
    TestPhaseModel,
    TestEntityModel,
    TestInterfaceModel,
    TestCommentModel,
    TestTaskModel
)


class BaseRouter(Router):
    pass


class DocumentsRouter(BaseRouter):
    namespace = "documents"
    url_part = "^documents/"


class EntitiesRouter(BaseRouter):
    namespace = "entities"
    url_part = "^entities/"


base_router = Router()
documents_router = DocumentsRouter()
entities_router = EntitiesRouter()

documents_router.register(TestDocumentModel, index=True)
documents_router.register(TestGroupModel)
documents_router.register(TestPhaseModel)
base_router.register(documents_router, index=True)

entities_router.register(TestEntityModel, index=True)
entities_router.register(TestInterfaceModel)
base_router.register(entities_router)

base_router.register(TestCommentModel)
base_router.register(TestTaskModel)
