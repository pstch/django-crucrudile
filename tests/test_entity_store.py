import mock
import inspect
import abc

from django.test import TestCase


from django_crucrudile.entities.store import(
    provides, EntityStoreMetaclass, EntityStore
)

class ProvidesTestCase(TestCase):
    def test_callable(self):
        self.assertTrue(callable(provides))

    def test_calls_register_class(self):
        kwargs = {'key': 'value'}
        mock_provided_arg = mock.Mock()
        mock_router_class = mock.Mock()

        provides(mock_provided_arg, **kwargs)(mock_router_class)

        self.assertTrue(mock_router_class.register_class.called)

        called_args, called_kwargs = list(
            mock_router_class.register_class.call_args
        )

        self.assertEqual(
            called_args,
            (mock_provided_arg,)
        )
        self.assertEqual(
            called_kwargs,
            kwargs
        )

class EntityStoreMetaclassTestCase(TestCase):
    store_metaclass = EntityStoreMetaclass

    def test_subclasses_abcmeta(self):
        self.assertTrue(
            issubclass(self.store_metaclass, abc.ABCMeta)
        )

    def test_copies_base_store(self):
        class StoreA(metaclass=self.store_metaclass):
            _base_store = ["test1", "test2"]

        class StoreB(StoreA):
            pass

        class StoreC(StoreB):
            _base_store = ["different"]

        self.assertFalse(StoreA._base_store is StoreB._base_store)
        self.assertTrue(StoreA._base_store == StoreB._base_store)
        self.assertFalse(StoreA._base_store is StoreC._base_store)
        self.assertFalse(StoreA._base_store == StoreC._base_store)

class EntityStoreTestCase(TestCase):
    def setUp(self):
        class TestEntityStore(EntityStore):
            pass

        self.store_class = TestEntityStore
        self.store = self.store_class()

    def test_has_metaclass(self):
        self.assertTrue(
            isinstance(self.store_class, EntityStoreMetaclass)
        )

    def test_get_register_map(self):
        self.assertEqual(self.store.get_register_map(), {})

    def test_get_register_class_map(self):
        self.assertEqual(
            self.store_class.get_register_class_map(), {}
        )

    def test_store_attr(self):
        self.assertEqual(
            self.store._store,
            []
        )

    def test_register_apply_map(self):
        mock_entity = mock.Mock()
        mock_mapping_value = mock.Mock()

        base_cls = type('ToRegisterBase', (), {})
        matching_cls = type('ToRegister', (base_cls, ), {})
        not_matching_cls = type('ToRegister', (), {})

        mapping = {base_cls: mock_mapping_value}

        # Register with mock entity, no mapping, not silent
        # Register with mock entity, no mapping
        self.assertEqual(
            self.store_class.register_apply_map(
                mock_entity, {}, silent=False
            ),
            mock_entity
        )

        # Register with mock entity, with mapping (without entity)
        self.assertRaises(
            LookupError,
            lambda : self.store_class.register_apply_map(
                mock_entity, mapping, silent=False
            )
        )
        self.assertFalse(mock_mapping_value.called)

        # Register with mock entity, no mapping
        self.assertEqual(
            self.store_class.register_apply_map(mock_entity, {}),
            mock_entity
        )

        # Register with mock entity, with mapping (without entity)
        self.assertEqual(
            self.store_class.register_apply_map(mock_entity, mapping),
            mock_entity
        )
        self.assertFalse(mock_mapping_value.called)

        # Register with class and mapping (with class)
        self.store_class.register_apply_map(matching_cls, mapping),
        self.assertTrue(mock_mapping_value.called)
        self.assertEqual(
            list(mock_mapping_value.call_args),
            [(matching_cls, ), {}]
        )

        # Reset mock object & mapping
        mock_mapping_value = mock.Mock()
        mapping = {base_cls: mock_mapping_value}

        # Register with class and mapping (without class)
        self.store_class.register_apply_map(not_matching_cls, mapping)
        self.assertFalse(mock_mapping_value.called)


        # Reset mapping, use iterable key
        mapping = {(base_cls, ): mock_mapping_value}

        # Register with mock entity and mapping (with iterable keys,
        # without entity)
        self.assertEqual(
            self.store_class.register_apply_map(mock_entity, mapping),
            mock_entity
        )
        self.assertFalse(mock_mapping_value.called)

        # Register with class and mapping (with iterable keys, with
        # class)
        self.store_class.register_apply_map(matching_cls, mapping),
        self.assertTrue(mock_mapping_value.called)
        self.assertEqual(
            list(mock_mapping_value.call_args),
            [(matching_cls, ), {}]
        )

        # Reset mock object & mapping
        mock_mapping_value = mock.Mock()
        mapping = {(base_cls, ): mock_mapping_value}

        # Register with class and mapping (with iterable keys, without
        # class)
        self.store_class.register_apply_map(not_matching_cls, mapping)
        self.assertFalse(mock_mapping_value.called)

        # Reset mock object & mapping (with None key)
        mock_mapping_value = mock.Mock()
        mapping = {None: mock_mapping_value}

        # Register with class and mapping (with None key, without class)
        self.store_class.register_apply_map(not_matching_cls, mapping),
        self.assertTrue(mock_mapping_value.called)
        self.assertEqual(
            list(mock_mapping_value.call_args),
            [(not_matching_cls, ), {}]
        )

    def test_register_class(self):
        register_cls = type('RegisteredClass', (), {})
        self.store_class.register_class(register_cls)
        self.assertEqual(
            self.store_class._base_store,
            [register_cls, ]
        )

    def test_register(self):
        register_cls = type('RegisteredClass', (), {})
        register_obj = register_cls()
        self.store.register(register_obj)
        self.assertEqual(
            self.store._store,
            [register_obj, ]
        )

    def test_get_register_class_map_kwargs(self):
        self.assertEqual(
            self.store_class.get_register_class_map_kwargs(),
            {}
        )

    def test_get_register_map_kwargs(self):
        self.assertEqual(
            self.store.get_register_map_kwargs(),
            {}
        )

    def test_get_base_store_kwargs(self):
        self.assertEqual(
            self.store.get_base_store_kwargs(),
            {}
        )

    def test_register_base_store(self):
        register_cls = mock.Mock()
        self.store_class.register_class(register_cls)
        self.store = self.store_class()
        self.assertTrue(register_cls.called)
        self.assertEqual(
            self.store._store,
            [register_cls.return_value, ]
        )
