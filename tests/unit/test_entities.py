import inspect
import mock
from nose.tools import assert_true, assert_raises, assert_equal

from django_crucrudile.entities import Entity


class EntityTestCase:
    entity_class = Entity

    def test_is_abstract(self):
        assert_true(
            inspect.isabstract(self.entity_class)
        )

    def test_init_fails(self):
        assert_raises(
            TypeError,
            self.entity_class
        )

    def test_index_attr(self):
        assert_equal(
            self.entity_class.index,
            False
        )

    def test_is_patterns_abstract(self):
        assert_true(
            self.entity_class.patterns.__isabstractmethod__
        )

    def test_str_tree_func_callable(self):
        assert_true(
            callable(self.entity_class.get_str_tree)
        )

    def test_init_sets_index(self):
        mock_index = mock.Mock()

        class TestConcreteEntity(Entity):
            def patterns(self, parents=None, add_redirect=True):
                pass

        entity = TestConcreteEntity(mock_index)

        assert_equal(
            entity.index,
            mock_index
        )
