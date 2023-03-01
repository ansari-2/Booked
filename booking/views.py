from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist



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
        if venue.event.category.type == 'Sports':
            return sports_seats(request,venue)
        topseats = Seats.objects.all().filter(venue = venue,price = 350)
        bottomseats = Seats.objects.all().filter(venue = venue,price = 200)
        return render(request,'booking/seats.html',{'topseats':topseats,'bottomseats':bottomseats}) 
   else:   
        if venue.event.category.type == 'Sports':
            return sports_seats(request,venue)
        seatnumber = 0   
        for each in range(100):
            seatnumber += 1
            topseats = Seats.objects.create(venue = venue ,number = seatnumber, price = 350)    
        for each in range(101,301):
            seatnumber += 1
            bottomseats = Seats.objects.create(venue = venue ,number = seatnumber, price = 200) 
        topseats = Seats.objects.all().filter(venue = venue,price = 350)
        bottomseats = Seats.objects.all().filter(venue = venue,price = 200)
        return render(request,'booking/seats.html',{'topseats':topseats,'bottomseats':bottomseats}) 
      
   
   
def choose_seats(request,id,id2): 
    venue = Venue.objects.get(id = id2)
    total = 0
    try:
      selected = Seats.objects.get(id = id, venue = venue,booked = False)
    except ObjectDoesNotExist:
           topseats = Seats.objects.all().filter(venue = venue,price = 350)
           bottomseats = Seats.objects.all().filter(venue = venue,price = 200)   
           return render(request,'booking/seats.html',{'total':total,'topseats':topseats,'bottomseats':bottomseats})   
    bill,created = Bill.objects.get_or_create(seat = selected,total = selected.price,user = request.user)
    user = Bill.objects.filter(user = request.user)
    for each in user:
       total += each.seat.price
    if venue.event.category.type == 'Sports':
            left = Seats.objects.all().filter(venue = venue,price = 500)
            bottom = Seats.objects.all().filter(venue = venue,price = 200)   
            top = Seats.objects.all().filter(venue = venue,price = 300)
            right = Seats.objects.all().filter(venue = venue,price = 400)   
            context = {'topseats':top,'bottomseats':bottom,'rightseats':right,'leftseats':left,'total':total}
            return render(request,'booking/sports_seats.html',context)
    topseats = Seats.objects.all().filter(venue = venue,price = 350)
    bottomseats = Seats.objects.all().filter(venue = venue,price = 200)   
    return render(request,'booking/seats.html',{'total':total,'topseats':topseats,'bottomseats':bottomseats})   

   

@permission_required('booking.view_tickets', login_url='login')  
def booked(request):
    booked = Bill.objects.all().filter(user = request.user)
    for each in booked:
        seats = Seats.objects.get(number = each.seat.number, venue = each.seat.venue)
        ticket,created = Tickets.objects.get_or_create(seat = seats,user = request.user)
        seats.booked = True
        seats.save()
    Bill.objects.all().delete() 
    tickets = Tickets.objects.all().filter(user = request.user)
    return render(request,'booking/paid.html',{'booked':tickets})
      

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
   
def sports_seats(request,venue):
     
    exists = Seats.objects.filter(venue = venue, number = 100)
    if exists:
        return render(request,'booking/sports_seats.html',display_sports_seats(request,venue))  
    seatnumber = 0
    for _ in range(100):
        seatnumber += 1
        topseats = Seats.objects.create(venue = venue ,number = seatnumber, price = 300)  
    for _ in range(100,201):
        seatnumber += 1
        bottomseats = Seats.objects.create(venue = venue ,number = seatnumber, price = 200)     
    for _ in range(201,301):
        seatnumber += 1
        rightseats = Seats.objects.create(venue = venue ,number = seatnumber, price = 400)  
    for _ in range(301,401):
        seatnumber += 1
        leftseats = Seats.objects.create(venue = venue ,number = seatnumber, price = 500)
    return render(request,'booking/sports_seats.html',display_sports_seats(request,venue))  

def display_sports_seats(request,venue):

    left = Seats.objects.all().filter(venue = venue,price = 500)
    bottom = Seats.objects.all().filter(venue = venue,price = 200)   
    top = Seats.objects.all().filter(venue = venue,price = 300)
    right = Seats.objects.all().filter(venue = venue,price = 400)  
    football = False
    cricket = False
    if venue.event.genre == 'Football':
        football = True
    elif venue.event.genre == 'Cricket':
        cricket = True     
    context = {'topseats':top,'bottomseats':bottom,'rightseats':right,'leftseats':left,'football':football,'cricket':cricket}
    return context

def display(request):
    return render(request,'booking/signup.html')

def userProfile(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        user_password = request.POST.get('password1') 
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        try:
            user = User.objects.get(username = user_name)
            print(user)
            context = 'the username already exists'
            return render(request , 'booking/already.html',{'context': context})
        except User.DoesNotExist:
            lst = []
            for each in profile.objects.values('phone'):
                lst.append(each.get('phone'))
            if phone in lst:
                context = 'the phonenumber already exist enter a different phone number '
                return render(request ,'booking/already.html',{'context':context})
            else:
                user = User.objects.create_user(username = user_name, password = user_password,email= email,first_name=first_name,last_name=last_name)
                profile.objects.create(user = user, phone =phone)
                return render(request,'booking/created.html')
