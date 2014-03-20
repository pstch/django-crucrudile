from django.db import models

from django_pstch_helpers.models import UserNamed, UserDescribed
from django_pstch_helpers.models.mixins import (
    ModelInfoMixin, AutoPatternsMixin,
    ListableModelMixin,
    FullModelActionsMixin
)

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
