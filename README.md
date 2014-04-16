django-crucrudile [![Build Status](https://travis-ci.org/pstch/django-crucrudile.svg?branch=crucrudile)](https://travis-ci.org/pstch/django-crucrudile) [![Coverage Status](https://coveralls.io/repos/pstch/django-crucrudile/badge.png?branch=crucrudile)](https://coveralls.io/r/pstch/django-crucrudile?branch=crucrudile)
=================

> `django-crucrudile` allows you to create "model mixins", that define possible actions for this model. Those model mixins allow the model to be able to generate its URL patterns by itself, so that they can be included in `urls.py` using just a call to the `get_url_patterns()` method of the model class. 

## Documentation

The documentation, available at [django-crucrudile.readthedocs.org](http://django-crucrudile.readthedocs.org/en/latest/), is automatically created from the docstrings present in the source code, using Sphynx (and some extensions).

## Example

Here, we create two **model mixins** : `Listable` and `Detailable`, and we set the url_args attribute of DetailView so that django-crucrudile knows that the URL should contain a named capture group for the ID of the object to view.

Then, we create a Django Model, in which we use `Listable` and `Detailable` as mixins.


```python
from django.db.models import Model
from django.generic.views import ListView, DetailView
from django_crucrudile.models.mixins import make_model_mixin

DetailView.url_args = ['(?P<pk>\d+)',]

Listable = make_model_mixin(ListView)
Detailable = make_model_mixin(DetailView)

class Book(Listable, Detailable, Model):
    pass
        
>> Book.get_views()
[ListView, DetailView]
    
>> Book.get_url_name(ListView)
'book-list'
    
>> Book.get_list_url()
'/book/list'
        
>> Book.get_url_patterns()
[<RegexURLPattern book-list book/list>,
 <RegexURLPattern book-detail book/detail/<pk>>]
```

The return value of `get_url_patterns()` can be used in `urls.py` (for example, in `patterns('', ..)`).

Here, `ListView` and `DetailView` can be standard generic views, or your own CBVs. As you can see, the only requirement is that, when a view needs an URL argument, it must be specified in the `url_args` attribute of the view class.

`make_model_mixin` automatically patches the given view with utility functions from `views.mixins.ModelActionMixin`, needed to have information about "what does the view do" (action name), and "what paths should point to it" (URLs specification). For more flexibility, it can be  better to redefine the views, to subclass `views.mixins.ModelActionMixin`, and to override the needed methods (see documentation).

It is also possible to create the model mixins by yourself (`make_model_mixin` is just a convenience function to automatically create model mixins based on a view) (see documentation).

`django-crucrudile` also provides a convenience function, `auto_patterns_for_app`, that can generate the URL patterns for each Model in an application (using `ContentType` to find the models), and that can be used directly in `urls.py`.

## Tests

`django-crucrudile` usually has a 100% code coverage, as its internals aren't really complicated. You can watch the latest results of the tests on [Travis-CI/pstch/django-crucrudile](https://travis-ci.org/pstch/django-crucrudile).

## Getting help

This is my first attempt at creating a (hopefully) useful Django application. If you're trying it out, and need some help, feel free to contact me at hugo@pstch.net ! Really, this will make me really happy :)

## Contributing

If you feel like you want to contribute to this project, please fork/send patches/submit pull requests ! The documentation and tests really need some improvement. This was my first time writing serious test cases, and my testing code is particularly ugly :(

`django-crucrudile` only consists of 4 files, with 2 of them being just utility functions (`utils.py` and `urls.py`). The two other files are what really makes it working :

* `models/mixins.py` :: Model mixins (one base class) and on-the-run mixin creator (function)
* `views/mixins.py` :: View mixins (one base class)
