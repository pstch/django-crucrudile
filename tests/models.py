from django.db import models
from django.db.models import Model

from django.generic.views import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django_pstch_helpers.models.mixins import make_model_mixin

class TestListableModel(make_model_mixin(ListView), Model):
    pass

class TestDetailableModel(make_model_mixin(DetailView), Model):
    pass

class TestCreatableModel(make_model_mixin(CreateView), Model):
    pass

class TestUpdatableModel(make_model_mixin(UpdateView), Model):
    pass

class TestDeletableModel(make_model_mixin(DeleteView), Model):
    pass
