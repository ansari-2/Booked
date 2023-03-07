from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail
from random import randint
import json
# from twilio.rest import Client
# import os




def login_(request):
    if request.method == 'GET':
        return render(request, 'booking/authenticate.html')
    if request.method == 'POST':
        username_ = request.POST.get('username', '')
        entered_password = request.POST.get('password', '')
        user = authenticate(username=username_, password=entered_password)
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

def submit(request):
    if request.method == 'POST': 
        user_otp = request.POST.get('otp','0000')
        otp = randint(1000,9999)
        user = profile.objects.get(user = request.user)
        subject = f'OTP Verification'
        message = f'{otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        if otp == int(user_otp):
            return render(request,'booking/created.html')
        else:
            return render(request,'booking/submit.html')
    return render(request,'booking/submit.html')    


      

def venues(request,id):
   venues = Venue.objects.all().filter(event = Event.objects.get(id = id))
   return render(request,'booking/display_venues.html',{'venues': venues})

def main(request):
   category = Category.objects.all()
   lst = []
   for each in Seats.objects.filter(booked = True):
       lst.append(each.venue.event.name)
   lst.sort()
   trends = set(lst)
   events = []
   for trending in trends:
       events.append(Event.objects.get(name = trending))      
   return render(request,'booking/main.html',{'categories':category,'trending': events})

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
      searched = request.POST.get('genre','action')
      if Category.objects.filter(type = searched):
          result = Event.objects.filter(category = Category.objects.get(type = searched))
          return render(request,'booking/display_events.html',{'events':result}) 
      if Event.objects.filter(name = searched):
          result = Event.objects.filter(name = searched) 
          return render(request,'booking/display_events.html',{'events':result}) 
      elif Event.objects.filter(language = searched):
          result = Event.objects.filter(language = searched) 
          return render(request,'booking/display_events.html',{'events':result})
      elif Event.objects.filter(time = searched):
          result = Event.objects.filter(time = searched) 
          return render(request,'booking/display_events.html',{'events':result})
      elif Event.objects.filter(genre = searched):
          result = Event.objects.filter(genre = searched) 
          return render(request,'booking/display_events.html',{'events':result})
      elif Venue.objects.filter(name = searched):
          result = Venue.objects.filter(name = searched) 
          return render(request,'booking/display_venues.html',{'venues':result}) 
      elif Venue.objects.filter(location = searched):
          result = Venue.objects.filter(location = searched) 
          return render(request,'booking/display_venues.html',{'venues':result})
      elif Venue.objects.filter(showtime = searched):
          result = Venue.objects.filter(showtime = searched) 
          return render(request,'booking/display_venues.html',{'venues':result}) 
      elif Seats.objects.filter(price = int(searched)):
          result = Seats.objects.filter(price = int(searched))  
          return render(request,'booking/seats.html',{'topseats':result})                            
      return render(request,'booking/notfound.html')
      
   
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
    if request.method == 'GET':
        return render(request,'booking/created.html')
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
            for each in profile.objects.values('email'):
                lst.append(each.get('email'))
            if email in lst:
                context = 'Email already exist enter a different email '
                return render(request ,'booking/already.html',{'context':context})
            else:
                user = User.objects.create_user(username = user_name, password = user_password,email= email,first_name=first_name,last_name=last_name)
                profile.objects.create(user = user, email = email,username = user_name)
                return render(request,'booking/created.html')
            
def test_total(request):
    if request.method == "POST":
        pass
        value_lst = request.POST['total']
        json_value = json.loads(value_lst)
        for each in json_value[1]:
            seats = Seats.objects.get(number = each, venue = json_value[2][0])
            ticket,created = Tickets.objects.get_or_create(seat = seats,user = request.user)
            seats.booked = True
            seats.save()
        tickets = Tickets.objects.all().filter(user = request.user)

        display = [f'Your booked tickets are:\n']
        number = 0
        for each in tickets:
            number += 1
            display.append(f'''{number}.Event Name: {each.seat.venue.event.name}
Venue: {each.seat.venue.name} {each.seat.venue.location}
Showtime: {each.seat.venue.showtime} \nSeat Number:{each.seat.number}\n\n''')
        all_tickets = '\n'.join(display)  
        print(request.user)                
        user = User.objects.get(username = request.user)
        subject = f'Hi {user.username}, thank you for choosing Booked.'
        message = f'{all_tickets}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        return render(request,'booking/paid.html',{'booked':tickets})


