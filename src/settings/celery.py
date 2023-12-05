import environ
from celery.schedules import crontab

import constants.task_names


__all__ = (
    'CELERY_TASK_ALWAYS_EAGER',
    'CELERY_BROKER_URL',
    'CELERY_RESULT_BACKEND',
    'BROKER_URL',
    'CELERY_TIMEZONE',
    'CELERY_BEAT_SCHEDULE',
    'CELERY_TASK_ROUTES',
)

env = environ.Env()


CELERY_TASK_ALWAYS_EAGER = env.bool('CELERY_TASK_ALWAYS_EAGER', default=False)
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://guest:pass@127.0.0.1:5672/')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = 'UTC'

# используется health-check
BROKER_URL = CELERY_BROKER_URL

CELERY_BEAT_SCHEDULE = {

}

CELERY_TASK_ROUTES = {

}
