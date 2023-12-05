import os

__all__ = (
    'DATABASES',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'bank-app'),
        'USER': os.environ.get('POSTGRES_USER', 'bank-app'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'bank-app'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}
