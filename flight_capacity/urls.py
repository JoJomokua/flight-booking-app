from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    #Home route
     path('', views.home, name='home'),
    
    #Available flights route
    path('flights/', views.flight_capacity, name = 'flight_capacity'),
   
    #New booking route
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),

    #Cancel route
    path('cancel/<int:flight_id>/', views.cancel_booking, name='cancel'),

    #Dashboard route
    path('dashboard/',views.dashboard, name='dashboard'),

    #Signup route
    path('signup/',views.signup, name='signup'),

    #Login route
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    #Logout route
    path('logout/',auth_views.LogoutView.as_view(next_page='home'), name='logout'),

   ]
