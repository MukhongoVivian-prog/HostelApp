from django import forms
from django.contrib.auth.models import User
from .models import Room, Landlord, Booking, Hostel


class RegistrationForm(forms.ModelForm):
    USER_TYPE_CHOICES = [
        ('landlord', 'Landlord'),
        ('student', 'Student'),
    ]

    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Ensure password is hashed
        if commit:
            user.save()
        return user


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'rent', 'is_available']
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'rent': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Landlord
        fields = ['profile_photo']
        widgets = {
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
class RoomPhotoForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_photo']
        widgets = {
            'room_photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['room'].queryset = Room.objects.filter(is_available=True)
class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = ['name', 'proximity_to_campus', 'amenities', 'address', 'image']