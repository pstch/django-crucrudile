import inspect
import mock

from django.test import TestCase

from django_crucrudile.entities import Entity

class EntityTestCase(TestCase):
    entity_class = Entity

    def test_is_abstract(self):
        self.assertTrue(
            inspect.isabstract(self.entity_class)
        )

    def test_init_fails(self):
        self.assertRaises(
            TypeError,
            self.entity_class
        )

    def test_index_attr(self):
        self.assertEqual(
            self.entity_class.index,
            False
        )

    def test_is_patterns_abstract(self):
        self.assertTrue(
            self.entity_class.patterns.__isabstractmethod__
        )

    def test_str_tree_func_callable(self):
        self.assertTrue(
            callable(self.entity_class.get_str_tree)
        )

    def test_init_sets_index(self):
        mock_index = mock.Mock()

        class TestConcreteEntity(Entity):
            def patterns(self, parents=None, add_redirect=True):
                pass

        entity = TestConcreteEntity(mock_index)

        self.assertEqual(
            entity.index,
            mock_index
        )
