import environ

__all__ = (
    'ENVIRONMENT',
    'ENVIRONMENT_PROD',
    'ENVIRONMENT_DEV',
    'ENVIRONMENT_LOCAL',
    'ENVIRONMENT_TESTING',
)

env = environ.Env()


ENVIRONMENT_PROD = 'prod'
ENVIRONMENT_DEV = 'dev'
ENVIRONMENT_LOCAL = 'local'
ENVIRONMENT_TESTING = 'testing'

ENVIRONMENT = env('ENVIRONMENT', default='dev')
