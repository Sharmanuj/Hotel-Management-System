from django.urls import path
from . import views
# from .views import CityAutocomplete

app_name = 'hotel'

urlpatterns = [
    path('add', views.AddHotel.as_view(), name='add'),
    path('CountryLookup', views.CountryLookup, name='CountryLookup'),
    path('RegionLookup/<int:pk>', views.RegionLookup, name='RegionLookup'),
    path('CityLookup/<int:pk>', views.CityLookup, name='CityLookup'),
    path('addplace/', views.AddPlace.as_view(), name='addplace'),
    path('CityAutocomplete/',views.CityAutocomplete.as_view(),name='light'),
    path('search', views.SearchHotel.as_view(), name='search-hotel'),
    path('HotelList/<int:city>/<slug:date>',views.ListHotel.as_view(), name='list-hotel'),
    path('GetHotel/', views.GetHotel.as_view(), name='get-hotel-list'),
    
]
