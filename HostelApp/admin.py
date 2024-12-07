from django.contrib import admin
from .models import Landlord, Student, Room, Booking, Hostel, Payment

admin.site.register(Landlord)
admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Hostel)
admin.site.register(Payment)
