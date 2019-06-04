from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import url
from . import views

# app_name='main'
urlpatterns = [
    # The field option name, should be unique as it is a unique identifier.
    # e.g. if you want to use the hyperlink of index page, don't use hardcoded url like
    # href="/main/" as if it is changed we have to change all the occurrences of it.
    # to solve this, use the value from name field. for above example use
    # href="{% url 'index' %}
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    # path('search', views.SearchHotel.as_view(), name='search-hotel'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),  # List of Rooms
    path('reservations/', views.ReservationListView.as_view(), name='reservations'),  # List of Reservations
    path('reservations1/', views.ReservationListView1.as_view(),name='reservations1'),  # week List of Reservations
    path('reservations2/', views.ReservationListView2.as_view(),name='reservations2'),  # month List of Reservations
    path('reservation3/', views.ReservationListView3.as_view(),name='reservations3'),  # search name List of Reservations
    # <int:pk> takes the argument sent in urls.
    # path('room/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),  # Detail of each room
    path('room<str:pk>', views.RoomDetailView.as_view(), name='room-detail'),
    # Detail of each reservation
    path('reservation/<str:pk>', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('customer/<str:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),  # Detail of each customer
    path('staff/<str:pk>', views.StaffDetailView.as_view(), name='staff-detail'),  # Detail of staff
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('guests/', views.GuestListView.as_view(), name='guest-list'),
    path('reserve/', views.reserve, name='reserve'),  # For reservation
    # path('Autocomplete/',views.Autocomplete.as_view(),name='light'),
    path('contact/', views.contact, name='contact'),
    path('Gallery/', views.Gallery, name='Gellery'),
    # path('search/', views.autocompleteModel, name='search'),
]
