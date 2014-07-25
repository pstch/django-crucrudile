import mock
import abc
from nose.tools import assert_true, assert_false, assert_raises, assert_equal


from django_crucrudile.entities.store import(
    provides, register_instances, register_class
)
class DecoratorTestMixin:
    decorator = None
    decorator_blank_args = [None]
    decorator_blank_kwargs = {}

    def test_callable(self):
        assert_true(callable(self.decorator))

    def test_returns_callable(self):
        assert_true(callable(self.decorator(
            *self.decorator_blank_args,
            **self.decorator_blank_kwargs
        )))


class ProvidesTestCase(DecoratorTestMixin):
    @property
    def decorator(self):
        return provides

    def test_calls_register_class(self):
        kwargs = {'key': 'value'}
        mock_provided_arg = mock.Mock()
        mock_router_class = mock.Mock()

        self.decorator(mock_provided_arg,
                       **kwargs)(mock_router_class)

        assert_true(
            mock_router_class.register_class.called
        )

        called_args, called_kwargs = list(
            mock_router_class.register_class.call_args
        )

        assert_equal(
            called_args,
            (mock_provided_arg,)
        )
        assert_equal(
            called_kwargs,
            kwargs
        )


class RegisterInstancesTestCase(DecoratorTestMixin):
    @property
    def decorator(self):
        return register_instances

    def test_patches_constructor(self):
        mock_store = mock.Mock()
        mock_store.register = mock_register = mock.Mock()
        mock_init = mock.Mock()
        mock_entity_class = type(
            'MockEntity',
            (),
            {'__init__': mock_init}
        )

        self.decorator(mock_store)(mock_entity_class)

        mock_entity_class()

        assert_true(mock_init.called)
        assert_true(mock_register.called)


class RegisterClassTestCase(DecoratorTestMixin):
    @property
    def decorator(self):
        return register_class

    def test_calls_register_class(self):
        mock_store_class = mock.Mock()
        mock_reg_cls = mock_store_class.register_class
        mock_entity_class = mock.Mock()

        self.decorator(mock_store_class)(mock_entity_class)

        assert_true(mock_reg_cls.called)
        assert_equal(
            list(mock_reg_cls.call_args),
            [(mock_entity_class,), {}]
        )
