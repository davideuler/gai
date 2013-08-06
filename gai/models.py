from django.db import models


class Url(models.Model):
    origin = models.URLField(max_length=2083)
    hash = models.CharField(max_length=40, unique=True)
    short = models.CharField(max_length=11, null=True, blank=True)
    access_count = models.PositiveIntegerField(default=0)
    created_by = models.GenericIPAddressField()
    created_on = models.DateTimeField(auto_now_add=True)


class AccessLog(models.Model):
    url = models.ForeignKey('Url', related_name='access_logs')
    ip = models.GenericIPAddressField()
    useragent = models.ForeignKey('UserAgent', related_name='access_logs')
    access_on = models.DateTimeField(auto_now_add=True)


class UserAgent(models.Model):
    hash = models.CharField(max_length=40, unique=True)
    text = models.TextField()
