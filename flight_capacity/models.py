from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class FlightCapacity(models.Model):
    flight_number = models.CharField(max_length=10)
    Date = models.DateField(max_length=10)
    Capacity = models.IntegerField()

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    passenger_name = models.CharField(max_length=15)
    passenger_email = models.EmailField()
    passenger_phone_number = models.IntegerField()

#Links the booking directly to a specific flight
    flight = models.ForeignKey(FlightCapacity, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger_name} - {self.passenger_email} - {self.passenger_phone_number} - {self.flight.flight_number} - {self.booking_date}"