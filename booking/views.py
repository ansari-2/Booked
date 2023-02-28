from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required



def login_(request):
    if request.method == 'GET':
        return render(request, 'booking/authenticate.html')
    if request.method == 'POST':
        username_ = request.POST.get('username', '')
        entered_password = request.POST.get('password', '')
        user = authenticate(username=username_, password=entered_password)
        print(user)
        if user is not None:
            login(request, user)
        return redirect('main')

def logout_(request):
    logout(request)
    return redirect('login')

def display_seats(request,id):
   venue = Venue.objects.get(id = id)
   exists = Seats.objects.filter(venue = venue, number = 100)
   if exists:
     allseats = Seats.objects.all().filter(venue = venue)
     return render(request,'booking/seats.html',{'allseats':allseats})
   else:   
    seatnumber = 0
    for each in range(300):
      seatnumber += 1
      seats = Seats.objects.create(venue = venue ,number = seatnumber, price = 200)  
    allseats = Seats.objects.all().filter(venue = venue)
    return render(request,'booking/seats.html',{'allseats':allseats}) 
      
   
   
def choose_seats(request,id,id2): 
      venue = Venue.objects.get(id = id2)
      showtime = venue.showtime
      name = venue.name
      total = 0
      selected = Seats.objects.get(id = id, venue = venue)
      bill = Bill.objects.create(seat = selected,total = selected.price,user = request.user)
      user = Bill.objects.filter(user = request.user)
      for each in user:
       total += each.seat.price
      allseats = Seats.objects.all().filter(venue = venue)
      return render(request,'booking/seats.html',{'allseats':allseats,'total':total}) 
  
   

@permission_required('booking.view_ticket', login_url='login')  
def booked(request):
    booked = Bill.objects.all().filter(user = request.user)
    for each in booked:
     seats = Seats.objects.get(number = each.seat.number, venue = each.seat.venue)
     ticket = Tickets.objects.create(seat = seats,user = request.user)
     seats.booked = True
     seats.save()
    Bill.objects.all().delete() 
    tickets = Tickets.objects.all()
    allseats = Seats.objects.all()
    return render(request,'booking/paid.html',{'allseats':allseats,'booked':tickets})
      

def venues(request,id):
   venues = Venue.objects.all().filter(event = Event.objects.get(id = id))
   return render(request,'booking/display_venues.html',{'venues': venues})

def main(request):
   category = Category.objects.all()
   return render(request,'booking/main.html',{'categories':category})

def explore(request,id):
   category = Category.objects.get(id = id)
   if category.type == 'Movie':
    movies = Event.objects.all().filter(category = Category.objects.get(type = 'Movie'))
    return render(request,'booking/display_events.html',{'events': movies})
   elif category.type == 'Event':
    event = Event.objects.all().filter(category = Category.objects.get(type = 'Event'))
    return render(request, 'booking/display_events.html',{'events':event})
   else:
    sport = Event.objects.all().filter(category = Category.objects.get(type = 'Sports'))
    return render(request, 'booking/display_events.html',{'events':sport})
   
def search_bar(request):
   if request.method == 'POST':
      genre = request.POST.get('genre','action')
      genre = genre.capitalize()
      event = Event.objects.all().filter(genre = genre)
      return render(request,'booking/display_events.html',{'events':event})
   return redirect('main')  
   