from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class IDC(models.Model):  # 机房
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.city.name}"


class Host(models.Model):
    hostname = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    root_password = models.CharField(max_length=100)
    idc = models.ForeignKey(IDC, on_delete=models.CASCADE)

    def __str__(self):
        return self.hostname


class HostStat(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    idc = models.ForeignKey(IDC, on_delete=models.CASCADE)
    count = models.IntegerField()
    stat_date = models.DateField(auto_now_add=True)


class HostPasswordHistory(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    root_password = models.CharField(max_length=100)
    changed_at = models.DateTimeField(auto_now_add=True)
