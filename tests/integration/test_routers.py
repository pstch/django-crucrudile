import hashlib

from django.test import TestCase
from django.db import models

from django_crucrudile.routers import (
    Router,
)


class EmptyRouterTestCase(TestCase):
    """#TODO"""
    def setUp(self):
        self.base_router = Router()

    def test_patterns_empty(self):
        list(self.base_router.patterns())


class TestDocumentModel(models.Model):
    pass


class TestGroupModel(models.Model):
    pass


class TestPhaseModel(models.Model):
    pass


class TestEntityModel(models.Model):
    pass


class TestInterfaceModel(models.Model):
    pass


class TestCommentModel(models.Model):
    pass


class TestTaskModel(models.Model):
    pass


class RouterTestCase(TestCase):
    """#TODO"""
    def setUp(self):
        self.base_router = Router()
        self.base_router.base = True

        self.documents_router = Router(
            namespace="documents",
            url_part="^documents/"
        )
        self.documents_router.register(TestDocumentModel, index=True)
        self.documents_router.register(TestGroupModel)
        self.documents_router.register(TestPhaseModel)

        self.base_router.register(
            self.documents_router,
            index=True
        )

        self.entities_router = Router(
            namespace="entities",
            url_part="^entities/"
        )

        self.entities_router.register(TestEntityModel, index=True)
        self.entities_router.register(TestInterfaceModel)

        self.base_router.register(
            self.entities_router
        )

        self.base_router.register(TestCommentModel)
        self.base_router.register(TestTaskModel)

    def _test_stores(self):
        self.assertEqual(
            self.base_router._store,
            [self.documents_router]
        )
        self.assertEqual(
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
        self.assertEqual(
            tree_hash,
            "7fc45b276e4f325044f2658f27acbc005974512564e377233c7f9b712bec2935"
        )

    def test_get_pydot_graph(self):
        self.base_router.get_pydot_graph()
        self.base_router.get_pydot_graph(recurse_limit=2)
