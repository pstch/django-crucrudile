from nose.tools import assert_true, assert_raises, assert_equal
import inspect
import mock

from django_crucrudile.routes.arguments import RouteArguments

class RouteArgumentsTestCase:
    arguments_class = RouteArguments
