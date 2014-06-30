from functools import partial
import mock


from django.test import TestCase

from django_crucrudile.routers import app
from django_crucrudile.routers.app import AppRouter


class AppRouterTestCase(TestCase):
    router_class = AppRouter
    mock_routing_module = None

    def _get_cls_with_fake_attr(self, attr_name, fake_attr=None, base=None):
        if fake_attr is None:
            fake_attr = mock.Mock()
        if base is None:
            base_cls = self.router_class
        else:
            base_cls = base

        router_class = type(
            base_cls.__name__,
            (base_cls,),
            {attr_name: fake_attr}
        )
        return router_class, fake_attr


    def setUp(self):
        (self.mocked_router_class,
         self.mock_routing_module) = self._get_cls_with_fake_attr(
            'get_routing_module',
             lambda x: self.mock_routing_module
        )
        self.mock_routing_module.entities = []


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

        router_class, mock_func = self._get_cls_with_fake_attr(
            'add_app_namespace', False, self.mocked_router_class
        )

        router = router_class(app_module_name="test1.test2")
        self.assertEqual(router.namespace, None)

    def test_init_calls_register_modules_entities(self):
        router_class, mock_func = self._get_cls_with_fake_attr(
            'register_module_entities',
            base=self.mocked_router_class
        )
        router = router_class(app_module_name="test")
        self.assertTrue(mock_func.called)

    def test_register_module_entities_not_silent(self):
        router_class, mock_func = self._get_cls_with_fake_attr(
            'register_module_entities',
            base=self.mocked_router_class,
        )
        router = router_class(app_module_name="test")
        self.assertRaises(
            ValueError,
            partial(
                self.router_class.register_module_entities,
                router, silent=False
            )
        )

    def test_get_routing_entities(self):
        router_class, mock_func = self._get_cls_with_fake_attr(
            'register_module_entities',
            base=self.mocked_router_class,
        )
        router = router_class(app_module_name="test")

        self.assertEqual(
            router.get_routing_entities(),
            self.mock_routing_module.entities
        )

    def test_register_module_entities_empty(self):
        router_class, mock_func = self._get_cls_with_fake_attr(
            'register_module_entities',
            base=self.mocked_router_class,
        )
        router = router_class(app_module_name="test")

        self.router_class.register_module_entities(
            router
        )

        self.assertEqual(
            router._store,
            []
        )

    def test_register_module_entities(self):
        router_class, mock_func = self._get_cls_with_fake_attr(
            'register_module_entities',
            base=self.mocked_router_class,
        )
        router = router_class(app_module_name="test")

        mock_list = [mock.Mock() for _ in range(3)]

        self.mock_routing_module.entities = list(mock_list)

        self.router_class.register_module_entities(
            router
        )

        self.assertEqual(
            router._store,
            mock_list
        )

        self.router_class.register_module_entities(
            router, silent=False
        )

        self.assertEqual(
            router._store,
            mock_list*2
        )

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

    def test_get_routing_module(self):
        router_class, mock_func = self._get_cls_with_fake_attr(
            'register_module_entities',
            base=self.router_class,
        )
        import_module_mock = mock.Mock()
        import_module_mock.entities = []
        app.import_module = lambda x: import_module_mock
        router = router_class(app_module_name="test")
        self.assertEqual(
            router.get_routing_module(),
            import_module_mock
        )
