from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def get_model_name(self):
        return self._meta.model_name


class Document(BaseModel):
    pass


class Group(BaseModel):
    pass


class Phase(BaseModel):
    pass


class Entity(BaseModel):
    pass


class Interface(BaseModel):
    pass


class Comment(BaseModel):
    pass


class Task(BaseModel):
    pass
