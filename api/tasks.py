import random
import string
from celery import shared_task
from django.utils import timezone
from .models import Host, IDC, HostStat, HostPasswordHistory


def generate_random_password(length: int = 12) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choices(chars, k=length))


@shared_task
def rotate_root_passwords():
    for host in Host.objects.all():
        new_pwd = generate_random_password()
        HostPasswordHistory.objects.create(host=host, root_password=host.root_password)
        host.root_password = new_pwd
        host.save()


@shared_task
def daily_host_stats():
    for idc in IDC.objects.select_related('city').all():
        count = idc.host_set.count()
        HostStat.objects.create(city=idc.city, idc=idc, count=count, stat_date=timezone.now())
