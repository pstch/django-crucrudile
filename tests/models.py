from django.db import models
from django.db.models import Model

from django_pstch_helpers.models import UserNamed, UserDescribed
from django_pstch_helpers.models.mixins import (
    ModelInfoMixin,
    AutoPatternsMixin,
    ListableModelMixin,
    FilteredListableModelMixin,
    DetailableModelMixin,
    CreatableModelMixin,
    SpecificCreatableModelMixin,
    UpdatableModelMixin,
    DeletableModelMixin,
    BaseModelActionsMixin,
    FullModelActionsMixin,
)

class TestListableModel(ListableModelMixin, Model):
    pass

class TestFilteredListableModel(ListableModelMixin, Model):
    pass

class TestDetailableModel(DetailableModelMixin, Model):
    pass

class TestCreatableModel(CreatableModelMixin, Model):
    pass

class TestSpecificCreatableModel(SpecificCreatableModelMixin, Model):
    pass

class TestUpdatableModel(UpdatableModelMixin, Model):
    pass

class TestDeletableModel(DeletableModelMixin, Model):
    pass

class TestBaseModelMixinsModel(BaseModelActionsMixin, Model):
    pass

class TestFullModelMixinsModel(FullModelActionsMixin, Model):
    pass

class Genre(BaseModelActionsMixin, UserDescribed):
    pass

class Author(FullModelActionsMixin, UserDescribed):
    pass

class Publisher(ListableModelMixin, UserNamed):
    pass

class Book(FullModelActionsMixin, UserDescribed):
    isbn = models.CharField(max_length=24)
    genre = models.ForeignKey(Genre)
    author = models.ForeignKey(Author)
    publisher = models.ForeignKey(Publisher)
