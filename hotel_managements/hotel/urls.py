from django.urls import path
from hotel import views
app_name="hotel"
urlpatterns = [
    path('home/',views.home,name='home'),
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('hotelier_dashboard/',views.hotelier_dashboard,name='hotelier_dashboard'),
    path('register_user/',views.register_user,name='register_user'),
    path('register_hotelier/',views.register_hotelier,name='register_hotelier'),
    path('login_user/',views.login_user,name='login_user'),
    path('login_hotelier/',views.login_hotelier,name='login_hotelier'),
    path('logout/',views.logouts,name='logout'),
    path('addhotel/',views.add_hotel,name='addhotel'),
    path('viewhotel/',views.view_hotel,name='viewhotel'),
    path('updatehotel<int:hotel_id>/',views.update_hotel,name='updatehotel'),
    path('deletehotel<int:hotel_id>/',views.delete_hotel,name='deletehotel'),
    path('viewbookings/',views.view_bookings,name='viewbookings'),
    path('searchhotels/',views.search_hotels,name='searchhotels'),
    path('book_hotel<int:hotel_id>/', views.book_hotel, name='book_hotel'),
    path('cancelbooking/',views.cancel_booking,name='cancelbooking'),

]
