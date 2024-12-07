from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Landlord Model
class Landlord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django User
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)  # Link to Django User
    name = models.CharField(max_length=100,default=1)  # Add the name field
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hostels')
    image = models.ImageField(upload_to='hostels/', blank=True, null=True)
    proximity_to_campus = models.CharField(max_length=255)
    amenities = models.TextField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Room(models.Model):
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, related_name='rooms')  # One landlord can have multiple rooms
    room_number = models.CharField(max_length=10)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    booked_by = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True)
    room_photo = models.ImageField(upload_to='room_photos/', null=True, blank=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, null=True, blank=True)  # Made nullable

    def __str__(self):
        return f"Room {self.room_number} - {self.landlord.user.username}"


class Booking(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')

    def __str__(self):
        return f"Booking by {self.student.name} for room {self.room.room_number}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')  # Changed room -> booking
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Payment {self.id} for Booking {self.booking.id} - {self.status}"
