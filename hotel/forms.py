from django import forms
from .models import Place, Hotel
from dal import autocomplete
from cities_light.models import City


class AddHotelForm(forms.ModelForm):
    class Meta:
        model=Hotel
        fields = ['Name', 'place']

    def __init__(self, **kwargs):
        user = kwargs.pop('user')
        super(AddHotelForm, self).__init__(**kwargs)
        self.fields['place'].queryset = Place.objects.filter(user=user)


class AddPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['address', 'country', 'region', 'city']


class SearchHotelForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    # co = forms.ModelChoiceField(
    #     queryset=City.objects.all(),
    #     widget=autocomplete.Select2(url='/hotel/CityAutocomplete/')
    # )

    class Meta:
        model = Place
        fields = ['city']
        widgets = {
            'city': autocomplete.Select2(url='/hotel/CityAutocomplete/')
            }
    # class Meta:
    #     model = Place
    #     fields = ['city']
    #     widgets = {
    #         'city': autocomplete.ModelSelect2(url='hotel:light')
    #     }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].widget.attrs.update(
            {"class": "browser-default custom-select"})
        # self.fields['city'].queryset=City.objects.all()
