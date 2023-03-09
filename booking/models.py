from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    type = models.CharField(max_length=100)
    image = models.CharField(max_length=100,null=True,blank = True )
    
    def __str__(self):
        return f'Type: {self.type} Image:{self.image}'       

class Event(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    ratings= models.FloatField(default=0)
    language = models.CharField(max_length=100)
    time = models.CharField(max_length=50)
    image = models.CharField(max_length=256)
    genre = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Category:{self.category}, name: {self.name},ratings: {self.ratings},language:{self.language},time: {self.time},image:{self.image}'
    
class Venue(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    location = models.CharField(max_length=256)
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=256)
    showtime = models.CharField(max_length=256)
    
    def __str__(self):
        return f'event:{self.event}, location: {self.location}, name: {self.name}, logo:{self.logo}, showtime: {self.showtime}'

class Seats(models.Model):
    venue = models.ForeignKey(Venue,on_delete=models.CASCADE)
    number = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    booked = models.BooleanField(default=False)
    def __str__(self) -> str:
        return f'Venue:{self.venue}Number:{self.number} Price:{self.price} booked:{self.booked}'
    
class Bill(models.Model):
    seat = models.ForeignKey(Seats,on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    def __str__(self) -> str:
        return f'{self.seat},{self.total},{self.user},{self.venue}'
    
class Tickets(models.Model):
    seat = models.ForeignKey(Seats,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)

class profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE) 
    email = models.CharField(max_length=100,blank = True,null = True)
    username = models.CharField(max_length= 100,blank=True,null=True)




