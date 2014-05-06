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

__title__ = 'django-crucrudile'
__description__ = 'Model-defined CRUD views & patterns for Django',

__version__ = '0.4.7'

__author__ = 'Hugo Geoffroy'
__author_email__ = 'hugo@pstch.net'

__license__ = 'GNU General Public License V3.0'
__copyright__ = 'Copyright 2013-2014 Hugo Geoffroy'
__url__ = 'https://github.com/pstch/django-crucrudile'
