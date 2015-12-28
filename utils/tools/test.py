from celery import Celery
from celery.schedules import crontab
import datetime

app = Celery('test')

# import celeryconfig
# app.config_from_object('celeryconfig')

app.conf.update(
  BROKER_URL='redis://172.20.14.29:6379/0',
  CELERY_RESULT_BACKEND='redis://172.20.14.29:6379/0',
  CELERY_TASK_SERIALIZER='json',
  CELERY_ACCEPT_CONTENT=['json'],
  CELERY_RESULT_SERIALIZER='json',
  CELERY_TIMEZONE='Asia/Shanghai',
  CELERY_ENABLE_UTC=False,
  CELERYBEAT_SCHEDULE={
    'add-every-30-seconds': {
        'task': 'test.add',
        'schedule': datetime.timedelta(seconds=30),
        'args': (16, 16)
    },
    # 'add-every-minutes': {
    #     'task': 'test.mul',
    #     'schedule': crontab(),
    #     'args': (16, 16),
    # },
  }
)


@app.task(bind=True)
def add(self, x, y):
  print '#'*50
  print self.request.id
  print self.request.hostname
  print '#'*50
  return x + y


@app.task
def mul(x, y):
  return x * y
