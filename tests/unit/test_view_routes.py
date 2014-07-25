# ~/code/django-crucrudile/django_crucrudile/routes/view.py

from nose.tools import assert_true, assert_raises, assert_equal
import mock

from django_crucrudile.routes import Route, ViewRoute


class ViewRouteTestCase:
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
        assert_true(
            issubclass(self.route_class, Route)
        )

    def test_init_requires_view_class(self):
        assert_raises(
            ValueError,  # No ``view_class``...
            self.route_class
        )

        view_class = mock.Mock()

        assert_equal(
            self.route_class(view_class=view_class).view_class,
            view_class
        )

        _route_class = type(
            'ViewRoute',
            (self.route_class, ),
            {'view_class': view_class}
        )

        assert_equal(
            _route_class().view_class,
            view_class
        )

    def test_view_class_attr(self):
        assert_equal(
            self.route.view_class,
            self.mock_view
        )

    def test_get_view_kwargs(self):
        assert_equal(
            self.route.get_view_kwargs(),
            {}
        )
