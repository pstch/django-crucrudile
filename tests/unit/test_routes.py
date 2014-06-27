import inspect
import mock

from django.test import TestCase

from django.core.urlresolvers import RegexURLPattern

from django_crucrudile.entities import Entity
from django_crucrudile.routes import (
    Route, ModelRoute,
    CallbackRoute, ViewRoute, ModelViewRoute
)


class RouteTestCase(TestCase):
    route_class = Route

    def test_is_abstract(self):
        self.assertTrue(
            inspect.isabstract(self.route_class)
        )

    def test_init_fails(self):
        self.assertRaises(
            TypeError,
            self.route_class
        )

    def test_subclasses_entity(self):
        self.assertTrue(
            issubclass(self.route_class, Entity)
        )

    def test_is_get_callback_abstract(self):
        self.assertTrue(
            self.route_class.get_callback.__isabstractmethod__
        )

    def test_name_attr(self):
        self.assertEqual(
            self.route_class.name,
            None
        )

    def test_url_part_attr(self):
        self.assertEqual(
            self.route_class.url_part,
            None
        )

    def test_auto_url_part_attr(self):
        self.assertEqual(
            self.route_class.auto_url_part,
            True
        )

    def test_init_requires_name(self):
        class TestConcreteRoute(self.route_class):
            def get_callback(self):
                pass

        self.assertRaises(
            ValueError,  # No ``name``...
            TestConcreteRoute
        )

        name = "test name"

        self.assertEqual(
            TestConcreteRoute(name=name).name,
            name
        )

        TestConcreteRoute.name = "test name (cls level)"

        self.assertEqual(
            TestConcreteRoute().name,
            TestConcreteRoute.name
        )

        TestConcreteRoute.auto_url_part = False

        self.assertRaises(
            ValueError,  # No ``url part`` and auto_url_part set to
                         # False...
            TestConcreteRoute
        )

        url_part = "test url part"

        self.assertEqual(
            TestConcreteRoute(url_part=url_part).url_part,
            url_part
        )

        TestConcreteRoute.url_part = "test url part (cls level)"

        self.assertEqual(
            TestConcreteRoute().url_part,
            TestConcreteRoute.url_part
        )

    def test_patterns_yields_url_pattern(self):
        mock_callback_getter = mock.Mock()

        class TestConcreteRoute(self.route_class):
            get_callback = mock_callback_getter

        route = TestConcreteRoute(name="name", url_part="urlpart")

        patterns = route.patterns()

        patterns = list(patterns)

        pattern = patterns.pop()

        self.assertEqual(
            patterns,
            []
        )

        self.assertTrue(
            isinstance(pattern, RegexURLPattern)
        )

        self.assertTrue(
            mock_callback_getter.called
        )

    def test_get_url_parts(self):
        class TestConcreteRoute(self.route_class):
            get_callback = None

        url_part = "urlpart"

        route = TestConcreteRoute(name="name", url_part=url_part)

        self.assertEqual(
            list(route.get_url_parts()),
            [url_part, ]
        )

    def test_get_url_name(self):
        class TestConcreteRoute(self.route_class):
            get_callback = None

        name = "name"

        route = TestConcreteRoute(name=name, url_part="urlpart")

        self.assertEqual(
            route.get_url_name(),
            name
        )


class CallbackRouteTestCase(TestCase):
    route_class = CallbackRoute
    mock_callback = None

    def setUp(self):
        self.route_class = type(
            'CallbackRoute',
            (self.route_class, ),
            {'name': "test name"}
        )
        self.mock_callback = mock.Mock()
        self.route = self.route_class(
            callback=self.mock_callback, name="name"
        )

    def test_subclasses_route(self):
        self.assertTrue(
            issubclass(self.route_class, Route)
        )

    def test_init_requires_callback(self):
        self.assertRaises(
            ValueError,  # No ``callback``...
            self.route_class
        )

        callback = mock.Mock()

        self.assertEqual(
            self.route_class(callback=callback).callback,
            callback
        )

        _route_class = type(
            'CallbackRoute',
            (self.route_class, ),
            {'callback': callback}
        )

        self.assertEqual(
            _route_class().callback,
            callback
        )

    def test_get_callback(self):
        self.assertEqual(
            self.route.get_callback(),
            self.mock_callback
        )


class ViewRouteTestCase(TestCase):
    route_class = ViewRoute
    mock_view = None

    def setUp(self):
        self.route_class = type(
            'CallbackRoute',
            (self.route_class, ),
            {'name': "test name"}
        )
        self.mock_view = mock.Mock()
        self.route = self.route_class(
            view_class=self.mock_view
        )

    def test_subclasses_route(self):
        self.assertTrue(
            issubclass(self.route_class, Route)
        )

    def test_init_requires_view_class(self):
        self.assertRaises(
            ValueError,  # No ``view_class``...
            self.route_class
        )

        view_class = mock.Mock()

        self.assertEqual(
            self.route_class(view_class=view_class).view_class,
            view_class
        )

        _route_class = type(
            'ViewRoute',
            (self.route_class, ),
            {'view_class': view_class}
        )

        self.assertEqual(
            _route_class().view_class,
            view_class
        )

    def test_view_class_attr(self):
        self.assertEqual(
            self.route.view_class,
            self.mock_view
        )

    def test_get_view_kwargs(self):
        self.assertEqual(
            self.route.get_view_kwargs(),
            {}
        )


class ModelRouteTestCase(TestCase):
    route_class = ModelRoute

    def setUp(self):
        self.route_class = type(
            'ModelRoute',
            (self.route_class, ),
            {'name': "test name"}
        )
        self.concrete_class = type(
            'ModelRoute',
            (self.route_class, ),
            {'get_callback': None}
        )
        self.mock_model = mock.Mock()
        self.model_name = "test model name"
        self.mock_model._meta.model_name = self.model_name

    def test_is_abstract(self):
        self.assertTrue(
            inspect.isabstract(self.route_class)
        )

    def test_init_fails(self):
        self.assertRaises(
            TypeError,
            self.route_class
        )

    def test_subclasses_route(self):
        self.assertTrue(
            issubclass(self.route_class, Route)
        )

    def test_is_get_callback_abstract(self):
        self.assertTrue(
            self.route_class.get_callback.__isabstractmethod__
        )

    def test_model_attr(self):
        self.assertEqual(
            self.route_class.model,
            None
        )

    def test_init_requires_model(self):
        self.assertRaises(
            ValueError,  # No ``model``...
            self.concrete_class
        )

        self.assertEqual(
            self.concrete_class(model=self.mock_model).model,
            self.mock_model
        )

        concrete_class = type(
            'ModelRoute',
            (self.concrete_class, ),
            {'model': self.mock_model}
        )

        self.assertEqual(
            concrete_class().model,
            concrete_class.model
        )

    def test_get_url_parts(self):
        url_part = "urlpart"

        name = "route name"

        route = self.concrete_class(
            name=name,
            model=self.mock_model,
            url_part=url_part)

        self.assertEqual(
            list(route.get_url_parts()),
            ["^{}/{}$".format(self.model_name, url_part)]
        )

    def test_get_url_name(self):
        class TestConcreteRoute(self.route_class):
            get_callback = None

        name = "route name"

        route = self.concrete_class(
            name=name,
            model=self.mock_model,
            url_part="urlpart"
        )

        self.assertEqual(
            route.get_url_name(),
            "{}-{}".format(self.model_name, name)
        )

    def test_model_url_name(self):
        route = self.concrete_class(
            name="name",
            model=self.mock_model,
            url_part="urlpart"
        )

        self.assertEqual(
            route.model_url_name,
            self.model_name
        )

    def test_model_url_part(self):
        route = self.concrete_class(
            name="name",
            model=self.mock_model,
            url_part="urlpart"
        )

        self.assertEqual(
            route.model_url_part,
            self.model_name
        )


class ModelViewRouteTestCase(TestCase):
    route_class = ModelViewRoute

    def test_subclasses_view_and_model_route(self):
        self.assertTrue(issubclass(self.route_class, ViewRoute))
        self.assertTrue(issubclass(self.route_class, ModelRoute))

    def test_get_view_kwargs(self):
        model = mock.Mock()
        route = self.route_class(
            model=model,
            view_class=mock.Mock(),
            name="name"
        )

        self.assertEqual(
            route.get_view_kwargs(),
            {'model': model}
        )

    def _test_make_for_view(self, view_name, route_name):
        view_class = type(
            view_name,
            (),
            {}
        )
        new = self.route_class.make_for_view(
            view_class,
            test_attr='test value'
        )

        self.assertTrue(new is not self.route_class)
        self.assertTrue(issubclass(new, self.route_class))
        self.assertEqual(new.view_class, view_class)
        self.assertEqual(new.test_attr, 'test value')
        self.assertEqual(new.__name__, route_name)

    def test_make_for_view_stripping_view_name(self):
        self._test_make_for_view('TestView', 'TestRoute')

    def test_make_for_view_not_stripping_view_name(self):
        self._test_make_for_view('FooBar', 'FooBarRoute')
