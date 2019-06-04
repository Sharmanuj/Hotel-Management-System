from django.contrib import admin
from .models import *
# Registers the Hotels and review models on the Django Admin page
admin.site.register(Hotel)
admin.site.register(Place)
