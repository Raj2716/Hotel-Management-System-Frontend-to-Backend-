from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegistrationForm(UserCreationForm):
    name=models.CharField(max_length=255)
    mobile_number = forms.CharField(max_length=15)
    gmail_id = models.EmailField(max_length=254)
    class Meta:
        model = CustomUser
        fields = ['name','username', 'mobile_number','gmail_id', 'password1', 'password2']

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'ratings', 'available_rooms', 'price', 'amenities', 'bed_type']


