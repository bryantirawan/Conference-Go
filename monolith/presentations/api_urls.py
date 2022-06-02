from django.urls import path

from .api_views import (
    api_list_presentations,
    api_show_presentation,
    api_approve_presentation,
    api_reject_presentation,
)


urlpatterns = [
    path(
        "conferences/<int:conference_id>/presentations/",
        api_list_presentations,
        name="api_list_presentations",
    ),
    path(
        "presentations/<int:pk>/",
        api_show_presentation,
        name="api_show_presentation",
    ),
    path(
        "presentations/<int:pk>/approval/",
        api_approve_presentation,
        name="api_approve_presentation",
    ),
    path(
        "presentations/<int:pk>/rejection/",
        api_reject_presentation,
        name="api_reject_presentation",
    ),
]
