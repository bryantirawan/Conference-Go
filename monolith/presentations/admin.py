from django.contrib import admin

from .models import Presentation, Status


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass
