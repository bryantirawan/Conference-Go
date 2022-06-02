from django.contrib import admin

from .models import Badge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    pass
