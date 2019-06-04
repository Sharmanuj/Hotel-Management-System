from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.db.models import Q
from django import views
from datetime import time
from cities_light.models import Country, Region, City
from .forms import AddHotelForm, AddPlaceForm
from django.views import generic
from .models import *
from dal import autocomplete
# from your_countries_app.models import City


# Create your views here.


class AddHotel(LoginRequiredMixin, views.generic.edit.FormView):
    template_name = 'hotel/add.html'


    def get_form_kwargs(self):
        kwargs = super(AddHotel, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_form_class(self):
        form_class_name = AddHotelForm
        return form_class_name

    def get_success_url(self):
        return reverse('signup')


class AddPlace(LoginRequiredMixin, views.generic.edit.CreateView):
    model = Place
    form_class = AddPlaceForm
    template_name = 'hotel/addplace.html'

    def form_valid(self, form):
        print(self.request.user.id)
        form.instance.user = self.request.user
        return super(AddPlace, self).form_valid(form)
        return HttpResponseRedirect(reverse('signup'))

    def form_invalid(self, form):
        super().form_invalid(form)
        return render(self.request, 'hotel/addplace.html', {'form': form})

    def get_success_url(self):
        return reverse('signup')

def CountryLookup(request):
    cou = serializers.serialize('json', Country.objects.all())
    # print(cou)
    return JsonResponse(cou, safe=False)


def RegionLookup(request, pk):
    cou = serializers.serialize(
        'json', Region.objects.all().filter(country_id=pk))
    return JsonResponse(cou, safe=False)


def CityLookup(request, pk):
    cou = serializers.serialize(
        'json', City.objects.all().filter(region_id=pk))
    return JsonResponse(cou, safe=False)


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        print("+++++++")
        print(reverse("hotel:light"))
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class SearchHotel(views.generic.edit.FormView):
    # pass
    form_class = SearchHotelForm
    template_name = 'hotel/search.html'

    def get_success_url(self):
        city = City.objects.get(name=self.form.cleaned_data['city'])
        print(city.id)
        return reverse_lazy('hotel:list-hotel', args=[city.id, self.form.cleaned_data['date']])

    def form_valid(self, form):
        self.form = form
        print(form.cleaned_data['date'])
        return HttpResponseRedirect(self.get_success_url())


class ListHotel(views.generic.ListView):
    template_name = 'hotel/List.html'
    model = Hotel

    def get_queryset(self):
        print(self.kwargs['city'])
        return Hotel.objects.filter(place__city=self.kwargs["city"])


class GetHotel(views.generic.TemplateView):
    template_name = 'hotel/searchhotel.html'
    def get_context_data(self, **kwargs):
        context = super(GetHotel, self).get_context_data(**kwargs)
        context['hotels'] = "No Hotel Found"
        form = SearchHotelForm(self.request.POST)
        id = self.request.GET.get('city')
        if form.is_valid():
            # form.save()
            id = form.cleaned_data['city']
            date = form.cleaned_data['date']
            # weekday = calendar.day_name[date.weekday()]
            print(id)
            print(date)
        else:
            print('invalid')
            print(form.errors)
        if Hotel.objects.filter(place__city=id):
            print('Hotel found')
        context['hotels'] = Hotel.objects.filter(place__city=id)
        print(context['hotels'][0].id)
        
        # print(slots)
        # context['instrument'] = instrument
        # context['date'] = date
        # print(date)
        # context['slots'] = slots
        # import code
        # code.interact(local=dict(globals(), **locals()))

        return context
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)
