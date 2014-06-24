import random

from functools import partial

from django.test import TestCase
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver

from django_crucrudile.exceptions import (
    NoRedirectDefinedException
)

from django_crucrudile.routers import (
    Router, ModelRoute, Route, ModelRouter as BaseModelRouter,
    provides
)


class EmptyRouterTestCase(TestCase):
    """#TODO"""
    def setUp(self):
        self.base_router = Router()

    def test_patterns_empty(self):
        list(self.base_router.patterns())


class ModelRoute(ModelRoute):
    def patterns(self, *args, **kwargs):
        yield


class ListRoute(ModelRoute):
    name = "list"
    index = True


class DetailRoute(ModelRoute):
    name = "detail"


class CreateRoute(ModelRoute):
    name = "create"


class UpdateRoute(ModelRoute):
    name = "update"


class DeleteRoute(ModelRoute):
    name = "delete"


@provides(ListRoute)
@provides(DetailRoute)
@provides(CreateRoute)
@provides(UpdateRoute)
@provides(DeleteRoute)
class ModelRouter(BaseModelRouter):
    pass

class RouterTestCase(TestCase):
    """#TODO"""
    def setUp(self):
        def add_model_routers(base_router, models):
            for model, index in models.items():
                model_router = ModelRouter(model=model)
                base_router.register(model_router, index=index)

        self.base_router = Router()
        self.base_router.base = True

        self.documents_router = Router(
            namespace="documents", label="documents",
            name="documents", url_part="^documents/"
        )
        add_model_routers(
            self.documents_router,
            {'document': True, 'group': False, 'phase': False}
        )
        self.base_router.register(
            self.documents_router,
            index=True
        )

        self.entities_router = Router(
            namespace="entities", label="entities",
            name="entities", url_part="^entities/"
        )

        add_model_routers(
            self.entities_router,
            {'entity': True, 'interface': False}
        )
        self.base_router.register(
            self.entities_router
        )

        add_model_routers(
            self.base_router,
            {'comment': False, 'task': False}
        )

    def _test_stores(self):
        self.assertEqual(
            self.base_router._store,
            [self.documents_router]
        )
        self.assertEqual(
            self.documents_router._store,
            [self.dashboard_route]
        )

    def test_pattern_tree(self):
        return

        import pydot
        _graph = pydot.Dot(graph_type='graph')

        def pattern_add_edges(graph, pattern,
                              recursive=False, recurse_limit=None):
            def get_node(_pattern):
                if _pattern is None:
                    node = pydot.Node(
                        str(hash(id(pattern)
                             ))[-6:]
                    )
                    node.set_label("None")
                    graph.add_node(node)
                    return node
                if getattr(_pattern, 'namespace', None) is not None:
                    color = 'green'
                elif isinstance(_pattern, RegexURLPattern):
                    color = 'red'
                elif isinstance(_pattern, RegexURLResolver):
                    color = 'blue'
                else:
                    color = 'white'

                node = pydot.Node(
                    str(id(_pattern)),
                    style="filled",
                    fillcolor=color
                )

                namespace = getattr(_pattern, 'namespace', None)
                callback = getattr(_pattern, 'callback', None)
                redirect_url = getattr(_pattern, '_redirect_url_name', None)
                router = getattr(_pattern, 'router', None)
                model = getattr(router, 'model', None)
                regex = getattr(_pattern, 'regex', None)
                regex_pattern = regex.pattern if regex else None

                node.set_label(
                    '\n'.join(filter(None, [
                        'namespace is {}'.format(namespace)
                        if namespace else None,
                        'callback is {}'.format(callback.__name__)
                        if callback else None,
                        'redirect_url is {}'.format(redirect_url)
                        if redirect_url else None,
                        'router is {}'.format(router.__class__.__name__)
                        if router else None,
                        'model is {}'.format(model)
                        if model else None,
                        'URL part is {}'.format(regex_pattern)
                        if regex_pattern else None,
                    ]))
                )

                return node

            pattern_node = get_node(pattern)
            graph.add_node(pattern_node)

            for sub_pattern in getattr(pattern, 'url_patterns', []):
                node = get_node(sub_pattern)
                #graph.add_node(node)

                edge = pydot.Edge(
                    pattern_node,
                    node,
                )

                graph.add_edge(edge)

                if recursive and recurse_limit != 0:
                    if recurse_limit is not None:
                        recurse_limit -= 1
                    pattern_add_edges(
                        graph,
                        sub_pattern,
                        recursive, recurse_limit
                    )

        pattern_add_edges(
            _graph, next(self.base_router.patterns()),
            True, None
        )

        _graph.write_png("/home/pistache/example.png")
        _graph.write_dot("/home/pistache/example.dot")
