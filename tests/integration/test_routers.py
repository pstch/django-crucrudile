import hashlib
from nose.tools import assert_equal

from django.db import models

from django_crucrudile.routers import (
    Router as BaseRouter,
)


class DocumentModel(models.Model):
    pass


class GroupModel(models.Model):
    pass


class PhaseModel(models.Model):
    pass


class EntityModel(models.Model):
    pass


class InterfaceModel(models.Model):
    pass


class CommentModel(models.Model):
    pass


class TaskModel(models.Model):
    pass

class Router(BaseRouter):
    generic = True


class EmptyRouterTestCase:
    def setUp(self):
        self.base_router = Router()

    def test_patterns_empty(self):
        list(self.base_router.patterns())


class RouterTestCase:
    def setUp(self):
        self.base_router = Router()
        self.base_router.generic = True
        self.base_router.base = True

        self.documents_router = Router(
            namespace="documents",
            url_part="documents"
        )
        self.documents_router.register(DocumentModel, index=True)
        self.documents_router.register(GroupModel)
        self.documents_router.register(PhaseModel)

        self.base_router.register(
            self.documents_router,
            index=True
        )

        self.entities_router = Router(
            namespace="entities",
            url_part="entities"
        )

        self.entities_router.register(EntityModel, index=True)
        self.entities_router.register(InterfaceModel)

        self.base_router.register(
            self.entities_router
        )

        self.base_router.register(CommentModel)
        self.base_router.register(TaskModel)

    def _test_stores(self):
        assert_equal(
            self.base_router._store,
            [self.documents_router]
        )
        assert_equal(
            self.documents_router._store,
            [self.dashboard_route]
        )

    def test_get_str_tree(self):
        tree = self.base_router.get_str_tree()

        def _hash(text):
            return hashlib.sha256(text.encode()).hexdigest()

        sorted_tree = '\n'.join(sorted(tree.splitlines()))

        tree_hash = _hash(sorted_tree)

        # compare to reference hash
        assert_equal(
            tree_hash,
            "33e058d3ed3a0b25990b879a2c4943d760b57b04fab8fb11598ad0db12f169af"
        )
