import os
import logging

from celery._state import get_current_task
from celery import Celery, platforms
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitors.settings')

class Formatter(logging.Formatter):
    """Formatter for tasks, adding the task name and id."""

    def format(self, record):
        task = get_current_task()
        if task and task.request:
            record.__dict__.update(task_id='%s ' % task.request.id,
                                   task_name='%s ' % task.name)
        else:
            record.__dict__.setdefault('task_name', '')
            record.__dict__.setdefault('task_id', '')
        return logging.Formatter.format(self, record)


root_logger = logging.getLogger() # 返回logging.root
root_logger.setLevel(logging.DEBUG)


# 将日志输出到控制台
sh = logging.StreamHandler()
formatter = Formatter('[%(task_name)s%(task_id)s%(process)s %(thread)s %(asctime)s %(pathname)s:%(lineno)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
sh.setFormatter(formatter)
sh.setLevel(logging.INFO)
root_logger.addHandler(sh)


app = Celery("monitors")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# namespace='CELERY' means all celery-related configuration keys
# should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# allow root user to run celery
platforms.C_FORCE_ROOT = True

# schedules tasks
app.conf.update(CELERYBEAT_SCHEDULE={
    'task': {
        'task': 'audi.tasks.CheckAudiVoice',
        'schedule': timedelta(seconds=10),
        'args': ()
    }
})
