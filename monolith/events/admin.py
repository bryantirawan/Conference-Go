from django.contrib import admin

from .models import Conference, Location, State


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    pass
