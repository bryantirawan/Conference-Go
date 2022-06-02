from django.urls import path

from .api_views import api_list_accounts, api_account_detail

urlpatterns = [
    path("accounts/", api_list_accounts, name="api_list_accounts"),
    path(
        "accounts/<str:email>/",
        api_account_detail,
        name="api_account_detail",
    ),
]
