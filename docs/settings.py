DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_crucrudile',
    'tests',
)

MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
ROOT_URLCONF = 'tests.urls'
USE_TZ = True
SECRET_KEY = 'so long and thanks for all the fish'

