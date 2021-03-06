import os

from kombu import Queue

CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_TIME_LIMIT = 60 * 5
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_TASK_QUEUES = [Queue('default')]
CELERY_TASK_DEFAULT_QUEUE = 'default'
CELERY_TASK_DEFAULT_EXCHANGE = 'default'
CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'
CELERY_TASK_CREATE_MISSING_QUEUES = False

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
