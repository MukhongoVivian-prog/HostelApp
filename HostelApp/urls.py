
from django.contrib import admin
from django.urls import path

from HostelApp import views
from HostelApp import views  as auth_views


urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    # Registration and Login URLs
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),

    # Landlord Dashboard
    path('landlord/dashboard/', views.landlord_dashboard, name='landlord_dashboard'),
    path('landlord/add_room/', views.add_room, name='add_room'),
    path('landlord/upload_profile_photo/', views.upload_profile_photo, name='upload_profile_photo'),
    path('landlord/add_hostel/', views.add_hostel, name='add_hostel'),
    path('landlord/bookings/', views.landlord_bookings, name='landlord_bookings'),
    path('landlord/payments/', views.landlord_payments, name='landlord_payments'),

    # Student Dashboard
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # Hostels and Rooms
    path('hostels/', views.hostel_list, name='hostel_list'),
    path('hostels/<int:hostel_id>/rooms/', views.room_list, name='room-list'),

    # Room Booking and Confirmation
    path('book_room/<int:room_id>/', views.book_room, name='book_room'),
    path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),

    # Room Photos
    path('rooms/<int:room_id>/upload_photo/', views.upload_room_photo, name='upload_room_photo'),

    # List all rooms (for debugging purposes, if needed)

    path('rooms/', views.rooms, name='rooms'),
    path('accounts/login/', auth_views.LoginView, name='login'),
]
