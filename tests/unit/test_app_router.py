import mock

from django.test import TestCase

from django_crucrudile.routers.app import (
    AppRouter,
)


class AppRouterTestCase(TestCase):
    router_class = AppRouter
    mock_module = None

    def setUp(self):
        self.mock_module = mock.Mock()
        self.mock_module.entities = []

        self.mocked_router_class = type(
            self.router_class.__name__,
            (self.router_class,),
            {'get_routing_module': lambda x: self.mock_module}
        )

    def test_init_fails(self):
        self.assertRaises(
            TypeError,
            self.router_class
        )

    def test_init(self):
        router = self.mocked_router_class(
            app_module_name="test1.test2",
        )
        self.assertEqual(router.namespace, "test1:test2")
        router = self.mocked_router_class(
            app_module_name="test1.test2",
            add_app_namespace=False
        )
        self.assertEqual(router.namespace, None)
        router = type(
            self.mocked_router_class.__name__,
            (self.mocked_router_class,),
            {'add_app_namespace': False}
        )(app_module_name="test1.test2")
        self.assertEqual(router.namespace, None)


    def test_get_routing_module_path(self):
        router = self.mocked_router_class(
            app_module_name="test_app_module_name",
        )
        self.assertEqual(
            router.get_routing_module_path(),
            "test_app_module_name.routing"
        )
        router.routing_module_name = 'test_routing_module_name'
        self.assertEqual(
            router.get_routing_module_path(),
            "test_app_module_name.test_routing_module_name"
        )
