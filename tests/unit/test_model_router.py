from functools import partial
import mock

from django.test import TestCase

from django.db.models import Model
from django.views.generic import (
    View, ListView, DetailView,
    CreateView, UpdateView, DeleteView
)

from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from django_crucrudile.routes import ViewRoute, ModelViewRoute

from django_crucrudile.routers import (
    Router, BaseModelRouter, ModelRouter,
)

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

    def test_init_sets_url_part(self):
        mock_url_part = mock.Mock()

        router = self.router_class(
            model=self.mock_model,
            url_part=mock_url_part
        )

        self.assertEqual(
            router.url_part,
            mock_url_part
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