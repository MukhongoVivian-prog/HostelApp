from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegistrationForm, RoomForm, ProfilePhotoForm, RoomPhotoForm, BookingForm, HostelForm
from .models import Landlord, Student, Room, Booking, Hostel, Payment


# Landlord Dashboard View
@login_required
def landlord_dashboard(request):
    # Check if the logged-in user is a landlord
    if not Landlord.objects.filter(user=request.user).exists(): # Show a "403 Forbidden" page if not a landlord
     return render(request, 'landlord_dashboard.html')

@login_required
def landlord_bookings(request):
    try:
        landlord = Landlord.objects.get(user=request.user)
    except Landlord.DoesNotExist:

        return redirect('register')
    bookings = Booking.objects.filter(room__landlord=landlord)

    return render(request, 'landlord_bookings.html', {'bookings': bookings})
# View to display all payments for the landlord
@login_required
def landlord_payments(request):
    landlord = request.user.landlord
    payments = Payment.objects.filter(room__landlord=landlord)
    return render(request, 'landlord_payments.html', {'payments': payments})
# Student Dashboard View
@login_required
def student_dashboard(request):
    # Your logic for fetching rooms or student-specific data
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'student_dashboard.html', {'rooms': rooms})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user and get the user object
            user = form.save(commit=True)

            # Get the user type and create the corresponding profile (Landlord or Student)
            user_type = form.cleaned_data['user_type']


            # Log the user in after successful registration
            login(request, user)

            # Redirect to the respective dashboard
            if user_type == 'landlord':
                return redirect('landlord_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            print(form.errors)  # Debug: Print form errors to the console
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
def contact(request):
    return render(request, 'contact.html')


@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.landlord = request.user.landlord  # Assign the logged-in landlord
            room.save()
            return redirect('landlord_rooms')
    else:
        form = RoomForm()

    return render(request, 'add_room.html', {'form': form})
def rooms(request):
    print("Inside rooms view")
    rooms_list = Room.objects.all()
    if not rooms_list:
        print("No rooms found")
        return HttpResponse('No rooms available', status=404)

    print(f"Rooms found: {rooms_list}")
    return render(request, 'rooms.html', {'rooms': rooms_list})
def room_list(request, hostel_id):
    hostel = get_object_or_404(Hostel, id=hostel_id)
    rooms = Room.objects.filter(hostel=hostel, is_available=True)
    return render(request, 'room_list.html', {'hostel': hostel, 'rooms': rooms})
@login_required
def upload_profile_photo(request):
    landlord = request.user.landlord
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=landlord)
        if form.is_valid():
            form.save()
            return redirect('landlord_dashboard')
    else:
        form = ProfilePhotoForm(instance=landlord)

    return render(request, 'profile_photo.html', {'form': form})


def upload_room_photo(request, room_id):
    room = Room.objects.get(id=room_id, landlord=request.user.landlord)

    if request.method == 'POST':
        form = RoomPhotoForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Photo uploaded successfully!")
            return redirect('landlord_rooms')  # Redirect to the landlord rooms page after success
        else:
            messages.error(request, "There was an error uploading the photo.")
    else:
        form = RoomPhotoForm(instance=room)  # Initialize the form for GET request

    return render(request, 'room_photo.html', {'form': form, 'room': room})




@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.student != request.user.student:
        raise Http404("You are not authorized to view this booking confirmation.")
    booking = Booking.objects.filter(id=booking_id, student=request.user.student).first()

    if not booking:
        messages.error(request, "Booking not found or you are not authorized to view it.")
        return redirect('student_dashboard')
    return render(request, 'booking_confirmation.html', {'booking': booking})

def home(request):
    return render(request, 'home.html')
def hostel_list(request):
    hostels = Hostel.objects.all()

    # Filters for proximity and amenities
    proximity_filter = request.GET.get('proximity')
    amenities_filter = request.GET.get('amenities')

    if proximity_filter:
        hostels = hostels.filter(proximity_to_campus__icontains=proximity_filter)
    if amenities_filter:
        hostels = hostels.filter(amenities__icontains=amenities_filter)

    return render(request, 'hostel-list.html', {'hostels': hostels})

def add_hostel(request):
    if request.method == 'POST':
        form = HostelForm(request.POST, request.FILES)
        if form.is_valid():
            hostel = form.save(commit=False)
            hostel.landlord = request.user
            hostel.save()
            return redirect('landlord_dashboard')
    else:
        form = HostelForm()
    return render(request, 'add_hostel.html', {'form': form})
@login_required
def book_room(request, room_id):
    # Check if user is a student (assuming a OneToOneField linking the user to the student)
    if not hasattr(request.user, 'student'):
        messages.error(request, "Only students can book rooms.")
        return redirect('room_list')

    # Get the room object or return a 404 if not found
    room = get_object_or_404(Room, id=room_id)

    if not room.is_available:
        messages.error(request, "Room is already booked.")
        return redirect('room_list')

    try:
        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Create a booking entry
            booking = Booking.objects.create(
                student=request.user.student,
                room=room
            )
            # Mark the room as unavailable
            room.is_available = False
            room.save()

        messages.success(request, "Room booked successfully!")
        return redirect('booking_confirmation', booking_id=booking.id)

    except Exception as e:
        messages.error(request, f"An error occurred while booking the room: {e}")
        return redirect('room_list')


def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate and log the user in
            user = form.get_user()
            login(request, user)

            # Redirect to the appropriate dashboard based on user role
            if hasattr(user, 'landlord'):  # If the user has a landlord profile
                return redirect('landlord_dashboard')  # Redirect to landlord dashboard
            elif hasattr(user, 'student'):  # If the user has a student profile
                return redirect('student_dashboard')  # Redirect to student dashboard
            else:
                return redirect('home')  # Or redirect to a default page if user role is not recognized
    else:
        form = AuthenticationForm()  # Create an empty form

    return render(request, 'login.html', {'form': form})