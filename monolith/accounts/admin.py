from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# This is a relative import of user from the models
# module in the same directory ".models"
from .models import User


admin.site.register(User, UserAdmin)
