from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Hotels(models.Model):
    Name = models.CharField(max_length = 200)
    Address = models.CharField(max_length = 500)
    City = models.CharField(max_length = 200)
    Plase = models.CharField(max_length = 150)
    Country = models.CharField(max_length = 50)
    Mobile_number = models.CharField(max_length = 12)
    Description = models.TextField(max_length = 500)


    class Meta:
        verbose_name_plural = 'Hotels'

    def get_absolute_url(self):
        return reverse('hoteldetails', kwargs={'pk': self.pk})
    def __str__(self):
         return self.Name


class Review(models.Model):
    hotel = models.ForeignKey(Hotels, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    Comment = models.CharField(max_length = 200)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)


    class Meta:
        verbose_name_plural = 'Review'

        def __str__(self):
            return self.Name