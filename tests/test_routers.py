import hashlib
import mock

from django.test import TestCase
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from django.db.models import Model
from django.views.generic import (
    View, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from django_crucrudile.routes import ViewRoute, ModelViewRoute

from django_crucrudile.entities import Entity
from django_crucrudile.entities.store import EntityStore


from django_crucrudile.routers import (
    Router, BaseModelRouter, ModelRouter,
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

    def test_get_redirect_pattern_fails(self):
        self.assertRaises(
            ValueError,
            self.router.get_redirect_pattern
        )
        self.assertEqual(
            self.router.get_redirect_pattern(silent=True),
            None
        )

    def test_patterns(self):
        patterns = self.router.patterns()
        pattern = next(patterns)
        self.assertRaises(StopIteration, patterns.__next__)
        self.assertTrue(isinstance(pattern, RegexURLResolver))
        self.assertEqual(pattern.url_patterns, [])


class BaseModelRouterTestCase(TestCase):
    router_class = BaseModelRouter

    def setUp(self):
        self.mock_model = mock.Mock()
        self.router = self.router_class(model=self.mock_model)

    def test_subclasses_router(self):
        self.assertTrue(
            issubclass(self.router_class, Router)
        )

    def test_model_attr(self):
        self.assertEqual(self.router_class.model, None)

    def test_init_requires_model(self):
        self.assertEqual(
            self.router.model,
            self.mock_model
        )

        self.assertRaises(
            ValueError,  # No ``model``...
            self.router_class
        )

        self.assertEqual(
            self.router_class(model=self.mock_model).model,
            self.mock_model
        )

        router_class = type(
            'BaseModelRouter',
            (self.router_class, ),
            {'model': self.mock_model}
        )

        self.assertEqual(
            router_class().model,
            router_class.model
        )

    def test_get_register_map_kwargs(self):
        self.assertEqual(
            self.router.get_register_map_kwargs(),
            {'model': self.mock_model}
        )

    def test_get_base_store_kwargs(self):
        self.assertEqual(
            self.router.get_base_store_kwargs(),
            {'model': self.mock_model}
        )

    def test_get_register_map(self):
        self.assertEqual(
            self.router.get_register_map(),
            {
                (SingleObjectMixin, MultipleObjectMixin):
                ModelViewRoute,
                View: ViewRoute,
                Model: ModelRouter
            }
        )

    def test_get_register_class_map(self):
        self.assertEqual(
            self.router_class.get_register_class_map(),
            {
                (SingleObjectMixin, MultipleObjectMixin):
                ModelViewRoute.make_for_view,
            }
        )


class ModelRouterTestCase(TestCase):
    router_class = ModelRouter

    def test_subclasses_base_model_router(self):
        self.assertTrue(
            issubclass(self.router_class, BaseModelRouter)
        )

    def test_base_store(self):
        _base_routes = {
            'ListRoute': ListView,
            'DetailRoute': DetailView,
            'CreateRoute': CreateView,
            'UpdateRoute': UpdateView,
            'DeleteRoute': DeleteView
        }
        for route_class in self.router_class._base_store:
            self.assertTrue(
                route_class.__name__ in _base_routes
            )
            self.assertEqual(
                route_class.view_class,
                _base_routes[route_class.__name__]
            )
