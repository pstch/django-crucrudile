"""django-crucrudile allows you to create "model mixins", that define
possible actions for this model. Those model mixins allow the model to
be able to generate its URL patterns by itself, so that they can be
included in urls.py using just a call to the get_url_patterns() method
of the model class.

Modules :
-- models.mixins : model mixins and functions
-- views.mixins : view mixins
-- urls : automatic URL patterns functions
-- utils : utility functions

"""
