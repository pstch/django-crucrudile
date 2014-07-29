from nose.tools import assert_equal
from django.conf.urls import url, include

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .routers import base_router
from .models import (
    DocumentModel,
    GroupModel,
    PhaseModel,
    EntityModel,
    InterfaceModel,
    CommentModel,
    TaskModel
)


MODEL_NAME_DICT = {
    'documents': (DocumentModel,
                  GroupModel,
                  PhaseModel),
    'entities': (EntityModel,
                 InterfaceModel),
    None: (CommentModel,
           TaskModel)
}

ACTION_NAME_DICT = {
    'list': ListView,
    'detail': DetailView,
    'create': CreateView,
    'update': UpdateView,
    'delete': DeleteView,
}

ACTION_ARGS_DICT = {
    'list': None,
    'detail': ["42", r"slug-test-42"],
    'create': None,
    'update': ["42", r"slug-test-42"],
    'delete': ["42", r"slug-test-42"],
}


class ResolveTestCase:
    router = base_router

    def setUp(self):
        self.patterns = list(self.router.patterns())
        self.url = url(
            '^/',
            include(self.patterns),
        )

    def _test_model_view(self,
                         model_name, action_name, view_name, args,
                         prefix):
        if args:
            args = "/{}".format(args)
        else:
            args = ""
        if prefix:
            path = "/{}/{}/{}{}".format(prefix, model_name, action_name, args)
        else:
            path = "/{}/{}{}".format(model_name, action_name, args)

        try:
            match = self.url.resolve(
                path
            )
        except:
            import ipdb; ipdb.set_trace()

        assert_equal(
            match.func.__name__,
            view_name
        )

        assert_equal(
            match.url_name,
            "{}-{}".format(model_name, action_name)
        )

        assert_equal(
            match.namespace,
            (prefix or '')
        )

    def test_model_views(self):
        for prefix, models in MODEL_NAME_DICT.items():
            for model_class in models:
                model_name = model_class._meta.model_name
                for action_name, view_class in ACTION_NAME_DICT.items():
                    view_name = view_class.__name__
                    if ACTION_ARGS_DICT.get(action_name):
                        for args in ACTION_ARGS_DICT[action_name]:
                            yield (
                                self._test_model_view,
                                model_name, action_name,
                                view_name, args, prefix
                            )
                    else:
                        yield (
                            self._test_model_view,
                            model_name, action_name,
                            view_name, None, prefix
                        )
