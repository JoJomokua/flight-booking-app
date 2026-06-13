from django.contrib import admin
from .models import FlightCapacity  #  Import your model

# Register your model here so it shows up in the admin dashboard
admin.site.register(FlightCapacity)
