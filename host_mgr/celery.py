import os
from celery import Celery
from celery.schedules import crontab
from pathlib import Path

project_name = Path(__file__).resolve().parent.name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
app = Celery(project_name)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'rotate-passwords-every-8-hours': {
        'task': 'hosts.tasks.rotate_root_passwords',
        'schedule': crontab(minute=0, hour='*/8'),
    },
    'daily-host-stats-at-midnight': {
        'task': 'hosts.tasks.daily_host_stats',
        'schedule': crontab(minute=0, hour=0),
    },
}
