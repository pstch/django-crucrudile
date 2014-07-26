# ~/code/django-crucrudile/django_crucrudile/routes/callback.py

from nose.tools import assert_true, assert_raises, assert_equal
import mock

from django_crucrudile.routes import CallbackRoute


class CallbackRouteTestCase:
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
            callback=self.mock_callback
        )

    def test_init_requires_callback(self):
        assert_raises(
            ValueError,  # No ``callback``...
            self.route_class
        )

        callback = mock.Mock()

        assert_equal(
            self.route_class(callback=callback).callback,
            callback
        )

        _route_class = type(
            'CallbackRoute',
            (self.route_class, ),
            {'callback': callback}
        )

        assert_equal(
            _route_class().callback,
            callback
        )

    def test_get_callback(self):
        assert_equal(
            self.route.get_callback(),
            self.mock_callback
        )
