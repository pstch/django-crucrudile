# ~/code/django-crucrudile/django_crucrudile/routes/__init__.py

from nose.tools import assert_true, assert_raises, assert_equal
import inspect
import mock


from django.core.urlresolvers import RegexURLPattern

from django_crucrudile.entities import Entity
from django_crucrudile.routes import Route


class RouteTestCase:
    route_class = Route

    def test_is_abstract(self):
        assert_true(
            inspect.isabstract(self.route_class)
        )

    def test_init_fails(self):
        assert_raises(
            TypeError,
            self.route_class
        )

    def test_subclasses_entity(self):
        assert_true(
            issubclass(self.route_class, Entity)
        )

    def test_is_get_callback_abstract(self):
        assert_true(
            self.route_class.get_callback.__isabstractmethod__
        )

    def test_name_attr(self):
        assert_equal(
            self.route_class.name,
            None
        )

    def test_url_part_attr(self):
        assert_equal(
            self.route_class.url_part,
            None
        )

    def test_auto_url_part_attr(self):
        assert_equal(
            self.route_class.auto_url_part,
            True
        )

    def test_init_requires_name(self):
        class TestConcreteRoute(self.route_class):
            def get_callback(self):
                pass

        assert_raises(
            ValueError,  # No ``name``...
            TestConcreteRoute
        )

        name = "test name"

        assert_equal(
            TestConcreteRoute(name=name).name,
            name
        )

        TestConcreteRoute.name = "test name (cls level)"

        assert_equal(
            TestConcreteRoute().name,
            TestConcreteRoute.name
        )

        TestConcreteRoute.auto_url_part = False

        assert_raises(
            ValueError,  # No ``url part`` and auto_url_part set to
                         # False...
            TestConcreteRoute
        )

        url_part = "test url part"

        assert_equal(
            TestConcreteRoute(url_part=url_part).url_part,
            url_part
        )

        TestConcreteRoute.url_part = "test url part (cls level)"

        assert_equal(
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

        assert_equal(
            patterns,
            []
        )

        assert_true(
            isinstance(pattern, RegexURLPattern)
        )

        assert_true(
            mock_callback_getter.called
        )

    def test_get_url_regexs(self):
        class TestConcreteRoute(self.route_class):
            get_callback = None

        url_part = "urlpart"

        route = TestConcreteRoute(name="name", url_part=url_part)

        assert_equal(
            list(route.get_url_regexs()),
            ['^urlpart$', ]
        )

    def test_get_url_name(self):
        class TestConcreteRoute(self.route_class):
            get_callback = None

        name = "name"

        route = TestConcreteRoute(name=name, url_part="urlpart")

        assert_equal(
            route.get_url_name(),
            name
        )
