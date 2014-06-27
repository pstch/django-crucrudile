from django.conf.urls import url, include
from django.test import TestCase
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .routers import base_router
from .models import (
    TestDocumentModel,
    TestGroupModel,
    TestPhaseModel,
    TestEntityModel,
    TestInterfaceModel,
    TestCommentModel,
    TestTaskModel
)


MODEL_NAME_DICT = {
    'documents': (TestDocumentModel,
                  TestGroupModel,
                  TestPhaseModel),
    'entities': (TestEntityModel,
                 TestInterfaceModel),
    None: (TestCommentModel,
           TestTaskModel)
}

ACTION_NAME_DICT = {
    'list': ListView,
    'detail': DetailView,
    'create': CreateView,
    'update': UpdateView,
    'delete': DeleteView,
}


class ResolveTestCase(TestCase):
    router = base_router

    def setUp(self):
        self.patterns = list(self.router.patterns())
        self.url = url(
            '^/',
            include(self.patterns),
        )

    def _test_model_view(self, model, action, view_name, prefix=None):
        if prefix:
            path = "/{}/{}/{}".format(prefix, model, action)
        else:
            path = "/{}/{}".format(model, action)

        match = self.url.resolve(
            path
        )
        self.assertEqual(
            match.func.__name__,
            view_name
            )
        self.assertEqual(
            match.url_name,
            "{}-{}".format(model, action)
        )
        if prefix:
            self.assertEqual(
                match.namespace,
                prefix
            )

for prefix, models in MODEL_NAME_DICT.items():
    for model in models:
        model_name = model._meta.model_name
        for action_name, view_class in ACTION_NAME_DICT.items():
            view_name = view_class.__name__
            if prefix:
                func_name = 'test_resolve_{}_{}_{}'.format(
                    prefix,
                    model_name,
                    action_name
                )
            else:
                func_name = 'test_resolve_{}_{}'.format(
                    model_name,
                    action_name
                )

            def _test(self):
                self._test_model_view(
                    model_name,
                    action_name,
                    view_name,
                    prefix=prefix,
                )
            setattr(
                ResolveTestCase,
                func_name,
                _test
            )
