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

    def _test_model_view(self,
                         model_name, action_name, view_name,
                         prefix=None):
        if prefix:
            path = "/{}/{}/{}".format(prefix, model_name, action_name)
        else:
            path = "/{}/{}".format(model_name, action_name)

        match = self.url.resolve(
            path
        )

        self.assertEqual(
            match.func.__name__,
            view_name
            )
        self.assertEqual(
            match.url_name,
            "{}-{}".format(model_name, action_name)
        )
        if prefix:
            self.assertEqual(
                match.namespace,
                prefix
            )


for prefix, models in MODEL_NAME_DICT.items():
    for model_class in models:
        model_name = model_class._meta.model_name
        for action_name, view_class in ACTION_NAME_DICT.items():
            view_name = view_class.__name__

            def _make_test(model, action, view, prefix):
                if prefix:
                    func_name = 'test_resolve_{}_{}_{}'.format(
                        prefix,
                        model,
                        action
                    )
                else:
                    func_name = 'test_resolve_{}_{}'.format(
                        model,
                        action
                    )

                def _test(self):
                    return ResolveTestCase._test_model_view(
                        self,
                        model,
                        action,
                        view,
                        prefix,
                    )

                return func_name, _test

            setattr(
                ResolveTestCase,
                *_make_test(model_name, action_name, view_name, prefix)
            )
