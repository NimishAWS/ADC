from django.contrib import admin

from .models import AuthUsers, Blog

admin.site.register(AuthUsers)
admin.site.register(Blog)
