from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from .forms import UserRegistrationForm,HotelForm
from .models import Booking,Hotel
import datetime
from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

# Create your views here.

def home(request):
       return render(request,"home.html")

def user_dashboard(request):
        return render(request,"user_dashboard.html")

def hotelier_dashboard(request):
        return render(request,"hotelier_dashboard.html")

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return home(request)
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

def register_hotelier(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return home(request)
    else:
        form = UserRegistrationForm()
    return render(request, 'register_hotelier.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return user_dashboard(request) 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def login_hotelier(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return hotelier_dashboard(request) 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logouts(request):
    if request.user.is_authenticated:
        logout(request)
        return home(request)
    

def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.hotelier = request.user
            hotel.save()
            return hotelier_dashboard(request)
    else:
        form = HotelForm()
    return render(request, 'add_hotel.html', {'form': form})

def view_hotel(request):
	hotel = Hotel.objects.filter(hotelier=request.user)
	return render(request,"view_hotel.html",{'hotel':hotel})

def update_hotel(request,hotel_id): 
    h=Hotel.objects.get(id=hotel_id) 
    e1 = HotelForm(instance = h) 
    if request.method == "POST":
        e1=HotelForm(request.POST,instance = h)
        if e1.is_valid():
            e1.save()
            return view_hotel(request)
    return render(request,"update_hotel.html",{'hotel_update':e1})

def delete_hotel(request,hotel_id):
    hotel=Hotel.objects.get(id=hotel_id)
    if request.method=='POST':
            hotel.delete()
            return view_hotel(request)
    return render(request,"delete_hotel.html",{'hotel_delete':hotel})


def view_bookings(request):
    # Retrieve all bookings for hotels owned by the logged-in hotelier
    bookings = Booking.objects.filter(hotel__hotelier=request.user)
    current_date = timezone.now().date()
    upcoming_bookings = bookings.filter(check_in__gte=current_date)
    past_bookings = bookings.filter(check_out__lt=current_date)

    return render(request, 'view_bookings.html', {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings,
        'bookings_exist': bookings.exists()
    })

def search_hotels(request):
    if request.method == 'POST':
        location = request.POST['location'].upper()
        max_price = request.POST['max_price']
        preferences = [pref.upper() for pref in request.POST.getlist('preferences')]
        hotels = Hotel.objects.filter(location=location, price__lte=max_price, available_rooms__gt=0)
        filtered_hotels = [hotel for hotel in hotels if set(preferences).issubset(set(hotel.amenities.split(',')))]
        return render(request, 'search_results.html', {'hotels': filtered_hotels})
    return render(request, 'search_hotels.html')


def book_hotel(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)
    amenities_list = hotel.amenities.split(',')
    if request.method == 'POST':
        check_in = request.POST['check_in']
        check_out = request.POST['check_out']
        num_members = request.POST['num_members']
        selected_amenities = request.POST.getlist('amenities')
        check_in_date = datetime.datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.datetime.strptime(check_out, '%Y-%m-%d')
        num_days = (check_out_date - check_in_date).days
        total_price = hotel.price * num_days
        booking=Booking.objects.create(user=request.user, hotel=hotel, check_in=check_in, check_out=check_out, num_members=num_members, total_price=total_price)
        if booking:
            hotel.available_rooms -= 1
            hotel.save()
        return render(request, 'booking_success.html', {
            'booking': booking,
            'hotel': hotel,
            'users': request.user.name,
            'selected_amenities': selected_amenities
        })
    return render(request, 'book_hotel.html', {'hotel': hotel,'amenities_list': amenities_list})


def cancel_booking(request):
    bookings = Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        booking_id = request.POST['booking_id']
        booking = Booking.objects.get(id=booking_id)
        if booking:
            booking.hotel.available_rooms += 1
            booking.hotel.save()
            booking.delete()
        return user_dashboard(request)
    return render(request, 'cancel_bookings.html', {'bookings': bookings})