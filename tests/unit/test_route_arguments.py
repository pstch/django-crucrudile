from nose.tools import assert_true, assert_raises, assert_equal
import inspect
import mock

from django_crucrudile.routes.arguments.builder import ArgsBuilder

class ArgsBuilderTestCase:
    parser_class = ArgsBuilder
