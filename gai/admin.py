from django.contrib import admin

from gai.models import AccessLog, Url, UserAgent

admin.site.register(Url)
admin.site.register(AccessLog)
admin.site.register(UserAgent)