from functools import partial
import mock

from django.test import TestCase

from django.core.urlresolvers import RegexURLResolver
from django.db.models import Model
from django.views.generic import View

from django_crucrudile.entities import Entity
from django_crucrudile.entities.store import EntityStore

from django_crucrudile.routes import ViewRoute

from django_crucrudile.routers import (
    Router, ModelRouter
)


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
        self.assertEqual(self.router_class.namespace, None)

    def test_url_part_attr(self):
        self.assertEqual(self.router_class.url_part, None)

    def test_redirect_attr(self):
        self.assertEqual(self.router_class.redirect, None)

    def test_init(self):
        self.assertEqual(self.router.namespace, None)
        self.assertEqual(self.router.url_part, None)
        self.assertEqual(self.router.redirect, None)

        namespace = mock.Mock()
        url_part = mock.Mock()
        redirect = mock.Mock()
        add_redirect = mock.Mock()
        add_redirect_silent = mock.Mock()
        get_redirect_silent = mock.Mock()

        router = self.router_class(
            namespace,
            url_part,
            redirect,
            add_redirect,
            add_redirect_silent,
            get_redirect_silent,
        )

        self.assertEqual(router.namespace, namespace)
        self.assertEqual(router.url_part, url_part)
        self.assertEqual(router.redirect, redirect)
        self.assertEqual(router.add_redirect, add_redirect)
        self.assertEqual(router.add_redirect_silent, add_redirect_silent)
        self.assertEqual(router.get_redirect_silent, get_redirect_silent)

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

    def test_get_redirect_pattern_fails(self):
        self.assertRaises(
            ValueError,
            self.router.get_redirect_pattern
        )
        self.assertEqual(
            self.router.get_redirect_pattern(silent=True),
            None
        )
        self.router.get_redirect_silent = True
        self.assertEqual(
            self.router.get_redirect_pattern(),
            None
        )

    def test_patterns(self):
        patterns = self.router.patterns()
        pattern = next(patterns)
        self.assertRaises(StopIteration, patterns.__next__)
        self.assertTrue(isinstance(pattern, RegexURLResolver))
        self.assertEqual(pattern.url_patterns, [])

    def test_patterns_fails_no_redirect(self):
        self.assertRaises(
            ValueError,
            partial(
                next,
                self.router.patterns(add_redirect=True)
            )
        )
        self.assertTrue(
            isinstance(
                next(self.router.patterns(
                    add_redirect=True,
                    add_redirect_silent=True
                )),
                RegexURLResolver
            )
        )
        router = self.router_class(
            add_redirect=True
        )
        self.assertRaises(
            ValueError,
            partial(
                next,
                router.patterns()
            )
        )
        router = self.router_class(
            add_redirect=True,
            add_redirect_silent=True
        )
        self.assertTrue(
            isinstance(
                next(router.patterns()),
                RegexURLResolver
            )
        )
