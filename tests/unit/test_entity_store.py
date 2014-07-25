import mock
import abc
from nose.tools import assert_true, assert_false, assert_raises, assert_equal


from django_crucrudile.entities.store import(
    EntityStoreMetaclass, EntityStore,
)


class EntityStoreMetaclassTestCase:
    store_metaclass = EntityStoreMetaclass

    def test_subclasses_abcmeta(self):
        assert_true(
            issubclass(self.store_metaclass, abc.ABCMeta)
        )

    def test_copies_base_store(self):
        class StoreA(metaclass=self.store_metaclass):
            _base_store = ["test1", "test2"]

        class StoreB(StoreA):
            pass

        class StoreC(StoreB):
            _base_store = ["different"]

        assert_false(StoreA._base_store is StoreB._base_store)
        assert_true(StoreA._base_store == StoreB._base_store)
        assert_false(StoreA._base_store is StoreC._base_store)
        assert_false(StoreA._base_store == StoreC._base_store)


class EntityStoreTestCase:
    def setUp(self):
        class TestEntityStore(EntityStore):
            pass

        self.store_class = TestEntityStore
        self.store = self.store_class()

    def test_has_metaclass(self):
        assert_true(
            isinstance(self.store_class, EntityStoreMetaclass)
        )

    def test_get_register_map(self):
        assert_equal(self.store.get_register_map(), {})

    def test_get_register_class_map(self):
        assert_equal(
            self.store_class.get_register_class_map(), {}
        )

    def test_store_attr(self):
        assert_equal(
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
        assert_equal(
            self.store_class.register_apply_map(
                mock_entity, {}, silent=False
            ),
            mock_entity
        )

        # Register with mock entity, with mapping (without entity)
        assert_raises(
            LookupError,
            lambda: self.store_class.register_apply_map(
                mock_entity, mapping, silent=False
            )
        )
        assert_false(mock_mapping_value.called)

        # Register with mock entity, no mapping
        assert_equal(
            self.store_class.register_apply_map(mock_entity, {}),
            mock_entity
        )

        # Register with mock entity, with mapping (without entity)
        assert_equal(
            self.store_class.register_apply_map(mock_entity, mapping),
            mock_entity
        )
        assert_false(mock_mapping_value.called)

        # Register with class and mapping (with class)
        self.store_class.register_apply_map(matching_cls, mapping),
        assert_true(mock_mapping_value.called)
        assert_equal(
            list(mock_mapping_value.call_args),
            [(matching_cls, ), {}]
        )

        # Reset mock object & mapping
        mock_mapping_value = mock.Mock()
        mapping = {base_cls: mock_mapping_value}

        # Register with class and mapping (without class)
        self.store_class.register_apply_map(not_matching_cls, mapping)
        assert_false(mock_mapping_value.called)

        # Reset mapping, use iterable key
        mapping = {(base_cls, ): mock_mapping_value}

        # Register with mock entity and mapping (with iterable keys,
        # without entity)
        assert_equal(
            self.store_class.register_apply_map(mock_entity, mapping),
            mock_entity
        )
        assert_false(mock_mapping_value.called)

        # Register with class and mapping (with iterable keys, with
        # class)
        self.store_class.register_apply_map(matching_cls, mapping),
        assert_true(mock_mapping_value.called)
        assert_equal(
            list(mock_mapping_value.call_args),
            [(matching_cls, ), {}]
        )

        # Reset mock object & mapping
        mock_mapping_value = mock.Mock()
        mapping = {(base_cls, ): mock_mapping_value}

        # Register with class and mapping (with iterable keys, without
        # class)
        self.store_class.register_apply_map(not_matching_cls, mapping)
        assert_false(mock_mapping_value.called)

        # Reset mock object & mapping (with None key)
        mock_mapping_value = mock.Mock()
        mapping = {None: mock_mapping_value}

        # Register with class and mapping (with None key, without class)
        self.store_class.register_apply_map(not_matching_cls, mapping),
        assert_true(mock_mapping_value.called)
        assert_equal(
            list(mock_mapping_value.call_args),
            [(not_matching_cls, ), {}]
        )

    def test_register_class(self):
        register_cls = type('RegisteredClass', (), {})
        self.store_class.register_class(register_cls)
        assert_equal(
            self.store_class._base_store,
            [register_cls, ]
        )

    def test_register(self):
        register_cls = type('RegisteredClass', (), {})
        register_obj = register_cls()
        self.store.register(register_obj)
        assert_equal(
            self.store._store,
            [register_obj, ]
        )

    def test_get_register_class_map_kwargs(self):
        assert_equal(
            self.store_class.get_register_class_map_kwargs(),
            {}
        )

    def test_get_register_map_kwargs(self):
        assert_equal(
            self.store.get_register_map_kwargs(),
            {}
        )

    def test_get_base_store_kwargs(self):
        assert_equal(
            self.store.get_base_store_kwargs(),
            {}
        )

    def test_register_base_store(self):
        register_cls = mock.Mock()
        self.store_class.register_class(register_cls)
        self.store = self.store_class()
        assert_true(register_cls.called)
        assert_equal(
            self.store._store,
            [register_cls.return_value, ]
        )
