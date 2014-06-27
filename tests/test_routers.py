import hashlib
import mock

from django.test import TestCase
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.db.models import Model
from django.views.generic import View

from django_crucrudile.entities import Entity
from django_crucrudile.entities.store import EntityStore


from django_crucrudile.routers import (
    Router, BaseModelRouter, ModelRouter,
)

from django_crucrudile.routes import ViewRoute


class RouterTestCase(TestCase):
    router_class = Router

    def setUp(self):
        self.router = self.router_class()

    def test_subclasses_entity(self):
        self.assertTrue(
            issubclass(self.router_class, Entity)
        )

    def test_subclasses_entity_store(self):
        self.assertTrue(
            issubclass(self.router_class, EntityStore)
        )

    def test_namespace_attr(self):
        self.assertEqual(self.router.namespace, None)

    def test_url_part_attr(self):
        self.assertEqual(self.router.url_part, None)

    def test_redirect_attr(self):
        self.assertEqual(self.router.redirect, None)

    def test_init(self):
        self.assertEqual(self.router.namespace, None)
        self.assertEqual(self.router.url_part, None)
        self.assertEqual(self.router.redirect, None)

        namespace = mock.Mock()
        url_part = mock.Mock()
        redirect = mock.Mock()

        router = self.router_class(
            namespace,
            url_part,
            redirect
        )

        self.assertEqual(router.namespace, namespace)
        self.assertEqual(router.url_part, url_part)
        self.assertEqual(router.redirect, redirect)

    def test_get_register_map(self):
        self.assertEqual(
            self.router.get_register_map(),
            {
                Model: ModelRouter,
                View: ViewRoute
            }
        )

    def test_register_entity(self):
        entity = mock.Mock()

        self.router.register(entity)

        self.assertEqual(
            self.router._store,
            [entity, ]
        )

    def test_register_index_entity(self):
        entity = mock.Mock()
        entity.index = True

        self.router.register(entity)

        self.assertEqual(
            self.router._store,
            [entity, ]
        )
        self.assertEqual(
            self.router.redirect,
            entity
        )

    def test_register_as_index(self):
        entity = mock.Mock()

        self.router.register(entity, index=True)

        self.assertEqual(
            self.router._store,
            [entity, ]
        )
        self.assertEqual(
            self.router.redirect,
            entity
        )
