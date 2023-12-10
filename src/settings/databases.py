import os

__all__ = (
    'DATABASES',
)

BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + 'db.sqlite3',
    }
}

