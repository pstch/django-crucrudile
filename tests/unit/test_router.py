from functools import partial
import mock
from nose.tools import assert_true, assert_raises, assert_equal

from django.core.urlresolvers import RegexURLResolver
from django.db.models import Model
from django.views.generic import View

from django_crucrudile.entities import Entity
from django_crucrudile.entities.store import EntityStore

from django_crucrudile.routes import ViewRoute

from django_crucrudile.routers import (
    Router, ModelRouter
)


class RouterTestCase:
    router_class = Router

    def setUp(self):
        self.router = self.router_class()

    def test_subclasses_entity(self):
        assert_true(
            issubclass(self.router_class, Entity)
        )

    def test_subclasses_entity_store(self):
        assert_true(
            issubclass(self.router_class, EntityStore)
        )

    def test_namespace_attr(self):
        assert_equal(self.router_class.namespace, None)

    def test_url_part_attr(self):
        assert_equal(self.router_class.url_part, None)

    def test_redirect_attr(self):
        assert_equal(self.router_class.redirect, None)

    def test_init(self):
        assert_equal(self.router.namespace, None)
        assert_equal(self.router.url_part, None)
        assert_equal(self.router.redirect, None)

        namespace = mock.Mock()
        url_part = mock.Mock()
        redirect = mock.Mock()
        add_redirect = mock.Mock()
        add_redirect_silent = mock.Mock()
        get_redirect_silent = mock.Mock()

        router = self.router_class(
            namespace,
            url_part,
            redirect,
            add_redirect,
            add_redirect_silent,
            get_redirect_silent,
        )

        assert_equal(router.namespace, namespace)
        assert_equal(router.url_part, url_part)
        assert_equal(router.redirect, redirect)
        assert_equal(router.add_redirect, add_redirect)
        assert_equal(router.add_redirect_silent, add_redirect_silent)
        assert_equal(router.get_redirect_silent, get_redirect_silent)

    def test_get_register_map(self):
        assert_equal(
            self.router.get_register_map(),
            {
                Model: ModelRouter,
                View: ViewRoute
            }
        )

    def test_register_entity(self):
        entity = mock.Mock()

        self.router.register(entity)

        assert_equal(
            self.router._store,
            [entity, ]
        )

    def test_register_index_entity(self):
        entity = mock.Mock()
        entity.index = True

        self.router.register(entity)

        assert_equal(
            self.router._store,
            [entity, ]
        )
        assert_equal(
            self.router.redirect,
            entity
        )

    def test_register_as_index(self):
        entity = mock.Mock()

        self.router.register(entity, index=True)

        assert_equal(
            self.router._store,
            [entity, ]
        )
        assert_equal(
            self.router.redirect,
            entity
        )

    def test_get_redirect_pattern_fails(self):
        assert_raises(
            ValueError,
            self.router.get_redirect_pattern
        )
        assert_equal(
            self.router.get_redirect_pattern(silent=True),
            None
        )
        self.router.get_redirect_silent = True
        assert_equal(
            self.router.get_redirect_pattern(),
            None
        )

    def test_patterns(self):
        patterns = self.router.patterns()
        pattern = next(patterns)
        assert_raises(StopIteration, patterns.__next__)
        assert_true(isinstance(pattern, RegexURLResolver))
        assert_equal(pattern.url_patterns, [])

    def test_patterns_fails_no_redirect(self):
        assert_raises(
            ValueError,
            partial(
                next,
                self.router.patterns(add_redirect=True)
            )
        )
        assert_true(
            isinstance(
                next(self.router.patterns(
                    add_redirect=True,
                    add_redirect_silent=True
                )),
                RegexURLResolver
            )
        )
        router = self.router_class(
            add_redirect=True
        )
        assert_raises(
            ValueError,
            partial(
                next,
                router.patterns()
            )
        )
        router = self.router_class(
            add_redirect=True,
            add_redirect_silent=True
        )
        assert_true(
            isinstance(
                next(router.patterns()),
                RegexURLResolver
            )
        )
