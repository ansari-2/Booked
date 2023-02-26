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
        return redirect('movies')

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
      time = venue.showtime
      event = Event.objects.get(name = venue.event.name)
      request.session['total'] = 0
      selected = Seats.objects.get(id = id, venue = venue)
      bill = Ticket.objects.create(seat = selected,total = selected.price,user = request.user)
      for each in Ticket.objects.all().filter(user = request.user,seat = Seats.objects.get(venue = venue)):

       request.session['total'] += each.total
      allseats = Seats.objects.all().filter(venue = venue)
      return render(request,'booking/seats.html',{'allseats':allseats,'total':request.session['total']}) 
  
   

@permission_required('booking.view_ticket', login_url='login')  
def booked(request):
    booked = Ticket.objects.filter(user = request.user)
    for each in booked:
     seats = Seats.objects.get(number = each.seat.number, venue = each.seat.venue)
     seats.booked = True
     seats.save()
    allseats = Seats.objects.all()
    return render(request,'booking/paid.html',{'allseats':allseats,'booked':booked})
      

def movies(request):
   movies = Event.objects.all().filter(category = Category.objects.get(type = 'Movie'))
   return render(request,'booking/display_movies.html',{'movies': movies})


def venues(request,id):
   venues = Venue.objects.all().filter(event = Event.objects.get(id = id))
   return render(request,'booking/display_venues.html',{'venues': venues})

# , seat = Seats.objects.get(venue = Venue.objects.get(showtime = time,event = event))):