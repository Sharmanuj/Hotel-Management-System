from django.contrib.auth.models import User
from django.db import models
from address.models import AddressField
from cities_light.models import Country


# # Create your models here.


class Place(models.Model):
    def __str__(self):
        # return "{}_{}".format(self.user.username,self.address)
        return "{}".format(self.address)
    address = models.CharField(max_length=1024)
    city = models.ForeignKey('cities_light.City', on_delete=models.CASCADE)
    region = models.ForeignKey('cities_light.region', on_delete=models.CASCADE)
    country = models.ForeignKey('cities_light.Country', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Hotel(models.Model):
    Name = models.CharField(max_length=255)
    place = models.ForeignKey(Place,null=True, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='hotel_img/', default='images/hotel.png')

    def __str__(self):
        return "{}".format(self.Name)
    class Meta:
        app_label = 'hotel'

