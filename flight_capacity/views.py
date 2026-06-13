from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Import your custom database models and forms
from .models import FlightCapacity, Booking
from .forms import BookingForm

# 1. HOME VIEW
def home(request):
    """Renders the central landing page for the application."""
    return render(request, 'home.html')


#  2. AVAILABLE FLIGHTS LIST VIEW
def flight_capacity(request):
    "Fetches all flights from the database and renders them on a public list."""
    flights = FlightCapacity.objects.all()
    context = {
        'flights': flights,
    }
    return render(request, 'all_flights.html', context)


# 👤 3. USER REGISTRATION (SIGNUP) VIEW
def signup(request):
    """Handles creating a new user account using Django's secure built-in form."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()      # Saves user to auth_user table (hashes password automatically)
            login(request, user)    # Instantly logs the user in so they don't have to log in manually
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


#  4. SECURE USER DASHBOARD VIEW
@login_required # Only allows logged-in members to view this page
def dashboard(request):
    """Fetches and displays bookings belonging ONLY to the logged-in user."""
    # Relational Database Filter: Matches the 'user' column to the active user's ID
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'bookings': user_bookings})


# 5. SECURE FLIGHT BOOKING VIEW
@login_required # Prevents anonymous guest checkouts
def book_flight(request, flight_id):
    """Validates data, verifies seat capacity, and links bookings to accounts."""
    flight = get_object_or_404(FlightCapacity, pk=flight_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
  
        if form.is_valid():
            # Extract clean, validated data from the form object
            name = form.cleaned_data['name']  
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']

            # Double-check database column value for seat availability
            if flight.Capacity > 0:
                # Create the transaction record in the database
                Booking.objects.create(
                    user=request.user,  # Tie this ticket to this specific logged-in user!
                    passenger_name=name,
                    passenger_email=email,
                    passenger_phone_number=phone_number,
                    flight=flight
                )
                # Atomically reduce inventory capacity and save changes
                flight.Capacity -= 1
                flight.save()
                
                # Send the user straight to their dashboard to view their active ticket
                return render(request, 'booking_success.html', {'flight': flight})
            else:
                return render(request, 'booking_failed.html', {'flight': flight, 'error': 'No remaining seats.'})
    else:
        # SMART UX: Auto-fill the form with their account details so they don't have to re-type them!
        form = BookingForm(initial={
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email
        })
 
    # Handles both initial page rendering and re-rendering on validation failures
    return render(request, 'book_flight.html', {'flight': flight, 'form': form})


#  6. CANCEL BOOKING VIEW
def cancel_booking(request, flight_id):
    """Handles restoring flight inventory when a seat reservation is canceled."""
    flight = get_object_or_404(FlightCapacity, pk=flight_id)

    if request.method == 'POST':
        user_booking = Booking.objects.filter(user=request.user, flight=flight).first()
        # Simple proof-of-concept safety rule (Assuming 1000 is maximum capacity)
        if user_booking:
            user_booking.delete()  
            flight.Capacity += 1
            flight.save()
            return render(request, 'cancel.html', {'flight': flight,'success': True})
    else:
     return render(request, 'cancel.html', {
        'flight': flight,
        'success': False, 
        'error_msg': 'No matching booking found for this account.'
        })
    

    return redirect('dashboard')