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
    try:
       user = User.objects.get(username = request.user)
    except ObjectDoesNotExist:  
       user = False      
    if request.method == 'GET':
        return render(request, 'booking/authenticate.html',{'user':user})
    if request.method == 'POST':
        username_ = request.POST.get('username', '')
        entered_password = request.POST.get('password', '')
        user = authenticate(username=username_, password=entered_password)
        if user is not None:
            login(request, user)
        return redirect('main')    

def logout_(request):
    logout(request)
    return redirect('main')

def display_seats(request,id):
   venue = Venue.objects.get(id = id)
   exists = Seats.objects.filter(venue = venue, number = 100)
#    try:
#     user = User.objects.get(username = request.user)
#    except ObjectDoesNotExist:  
#        user = False    
   if exists:
        if venue.event.category.type == 'Sports':
            return sports_seats(request,venue)
        premium = Seats.objects.all().filter(venue = venue,price = 350)
        regular = Seats.objects.all().filter(venue = venue,price = 200)
        return render(request,'booking/seats.html',{'premium':premium,'regular':regular}) 
   else:   
        if venue.event.category.type == 'Sports':
            return sports_seats(request,venue)
        for number in range(1,101):
                premium = Seats.objects.create(venue = venue ,number = number, price = 350)  
        for number in range(101,301):
                regular = Seats.objects.create(venue = venue ,number = number, price = 200)
        premium = Seats.objects.all().filter(venue = venue,price = 350)
        regular = Seats.objects.all().filter(venue = venue,price = 200)        
        return render(request,'booking/seats.html',{'premium':premium,'regular':regular})    

   
# def choose_seats(request,id,id2): 
#     venue = Venue.objects.get(id = id2)
#     total = 0
#     try:
#       selected = Seats.objects.get(id = id, venue = venue,booked = False)
#     except ObjectDoesNotExist:
#            topseats = Seats.objects.all().filter(venue = venue,price = 350)
#            bottomseats = Seats.objects.all().filter(venue = venue,price = 200)   
#            return render(request,'booking/seats.html',{'total':total,'topseats':topseats,'bottomseats':bottomseats})   
#     bill,created = Bill.objects.get_or_create(seat = selected,total = selected.price,user = request.user)
#     user = Bill.objects.filter(user = request.user)
#     for each in user:
#        total += each.seat.price
#     if venue.event.category.type == 'Sports':
#             left = Seats.objects.all().filter(venue = venue,price = 500)
#             bottom = Seats.objects.all().filter(venue = venue,price = 200)   
#             top = Seats.objects.all().filter(venue = venue,price = 300)
#             right = Seats.objects.all().filter(venue = venue,price = 400)   
#             context = {'topseats':top,'bottomseats':bottom,'rightseats':right,'leftseats':left,'total':total}
#             return render(request,'booking/sports_seats.html',context)
#     topseats = Seats.objects.all().filter(venue = venue,price = 350)
#     bottomseats = Seats.objects.all().filter(venue = venue,price = 200)   
#     return render(request,'booking/seats.html',{'total':total,'topseats':topseats,'bottomseats':bottomseats})   

def submit(request):

    if request.method == 'POST': 
        otp = randint(1000,9999)
        print(otp)
        user = User.objects.get(username = request.user)
        subject = f'OTP Verification'
        message = f'{otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )
        value_lst = request.POST.get('total')
        json_value = json.loads(value_lst)
        total = json_value[0]
        venue_id = json_value[2][0]
        venue = Venue.objects.get(id=venue_id)
        seats = []
        for each in json_value[1]:
            seats.append(Seats.objects.get(venue = venue,number = each))
        gst =  total * 18//100
        discount = (total * 10//100)
        new_total = total + gst - discount    
        print(otp,value_lst)
    # try:
    #    user = User.objects.get(username = request.user)
    # except ObjectDoesNotExist:  
    #    user = False     
    context = {'venue':venue,'total':total,'seats':seats,'json_data':value_lst,'gst':gst,'discount':discount,'final':new_total,'otp':otp}
    return render(request,'booking/paynow.html', context) 


      

def venues(request,id):
   venues = Venue.objects.all().filter(event = Event.objects.get(id = id))
   try:
      user = User.objects.get(username = request.user)
   except ObjectDoesNotExist:  
       user = False 
   return render(request,'booking/display_venues.html',{'venues': venues,'user':user})

def main(request):
     
   category = Category.objects.all()
   lst = []
   trends = []
   dct = {}
   for each in Seats.objects.filter(booked = True):
       lst.append(each.venue.event.name)
   for each in lst:
       dct.update({each:lst.count(each)})
   for each in sorted(dct.values(),reverse=True):
       for key,value in dct.items():
           if each == value:
               trends.append(key)
   for each in trends:
       if trends.count(each) > 1:
           trends.remove(each)        
   events = []
   num = 0
   for trending in trends:
       num += 1
       events.append(Event.objects.get(name = trending)) 
       if num == 10:
           break  
   try:
    user = User.objects.get(username = request.user)
   except ObjectDoesNotExist:  
       user = False     
   return render(request,'booking/main.html',{'categories':category,'trending': events,'user':user})

def explore(request,id=0):
     
    language_filter = Event.objects.all().filter(category = id).values_list('language').distinct()
    rating_filter = Event.objects.all().filter(category = id).values_list('ratings').distinct()
    genre_filter = Event.objects.all().filter(category = id).values_list('genre').distinct()
    
    filter_context = {'Genre':genre_filter,'Language':language_filter,'Ratings':rating_filter}
    category = Category.objects.get(id = id)
    events = Event.objects.all().filter(category=id)
    json_value = json.dumps('[0]')
    try:
        user = User.objects.get(username = request.user)
    except ObjectDoesNotExist:
        user = False    
    if request.method == "POST":
        print('inside post NOW')
        json_value = request.POST.get('submitButton')
        print(json_value)
        json_lst = json.loads(json_value)
        
        if len(json_lst[0]) !=0:
            print('inhere json[0]')
            events = events.filter(category=id,genre__in=json_lst[0])
        # print(events)
        if len(json_lst[1]) !=0:
            events = events.filter(category=id,language__in=json_lst[1])
        # print(events)
        if len(json_lst[2]) !=0:
            events = events.filter(category=id,ratings__in=json_lst[2])
        # print(events,'here')  
    return render(request,'booking/filter.html',{'category_id':id,'events':events,'filter_context':filter_context,'json_data':json_value,'user':user})
    

def search_bar(request):
   if request.method == 'POST':
      searched = request.POST.get('genre','action')
      if Category.objects.filter(type = searched):
          result = Event.objects.filter(category = Category.objects.get(type = searched))
          return render(request,'booking/display_events.html',{'events':result,'searched':searched}) 
      if Event.objects.filter(name = searched):
          result = Event.objects.filter(name = searched) 
          return render(request,'booking/display_events.html',{'events':result,'searched':searched}) 
      elif Event.objects.filter(language = searched):
          result = Event.objects.filter(language = searched) 
          return render(request,'booking/display_events.html',{'events':result,'searched':searched})
      elif Event.objects.filter(time = searched):
          result = Event.objects.filter(time = searched) 
          return render(request,'booking/display_events.html',{'events':result,'searched':searched})
      elif Event.objects.filter(genre = searched):
          result = Event.objects.filter(genre = searched) 
          return render(request,'booking/display_events.html',{'events':result,'searched':searched})
      elif Venue.objects.filter(name = searched):
          result = Venue.objects.filter(name = searched) 
          return render(request,'booking/display_venues.html',{'venues':result,'searched':searched}) 
      elif Venue.objects.filter(location = searched):
          result = Venue.objects.filter(location = searched) 
          return render(request,'booking/display_venues.html',{'venues':result,'searched':searched})
      elif Venue.objects.filter(showtime = searched):
          result = Venue.objects.filter(showtime = searched) 
          return render(request,'booking/display_venues.html',{'venues':result,'searched':searched}) 
    #   elif Seats.objects.filter(price = int(searched)):
    #       result = Seats.objects.filter(price = int(searched))  
            # return render(request,'booking/seats.html',{'topseats':result})                            
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
    # # try:
    # #    user = User.objects.get(username = request.user)
    # # except ObjectDoesNotExist:  
    #    user = False      
    if venue.event.genre == 'Football':
        football = True
    elif venue.event.genre == 'Cricket':
        cricket = True     
    context = {'topseats':top,'bottomseats':bottom,'rightseats':right,'leftseats':left,'football':football,'cricket':cricket}
    return context

def display(request):
    try:
       user = User.objects.get(username = request.user)
    except ObjectDoesNotExist:  
       user = False      
    return render(request,'booking/signup.html',{'user':user})

def userProfile(request):
    if request.method == 'GET':
        return render(request,'booking/already.html')
    if request.method == "POST":
        user_name = request.POST.get('username')
        user_password = request.POST.get('password1') 
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        try:
            user = User.objects.get(username = user_name)
            try:
               user_e = User.objects.get(username = request.user)
            except ObjectDoesNotExist:  
               user_e = False  
            context = 'the username already exists'
            return render(request , 'booking/already.html',{'context': context,'user':user_e})
        except User.DoesNotExist:
            try:
              user_e = User.objects.get(username = request.user)
            except ObjectDoesNotExist:  
              user_e = False  
            lst = []
            for each in profile.objects.values('email'):
                lst.append(each.get('email'))
            if email in lst:
                context = 'Email already exist enter a different email '
                return render(request ,'booking/already.html',{'context':context,'user':user_e})
            else:
                user = User.objects.create_user(username = user_name, password = user_password,email= email,first_name=first_name,last_name=last_name)
                profile.objects.create(user = user, email = email,username = user_name)
                return render(request,'booking/already.html',{'user':user_e})
            
def test_total(request):

    if request.method == "POST":
        value_lst = request.POST['total']
        json_value = json.loads(value_lst)
        seat_lst = []
        for each in json_value[1]:
            seats = Seats.objects.get(number = each, venue = json_value[2][0])
            seat_lst.append(seats)
            ticket,created = Tickets.objects.get_or_create(seat = seats,user = request.user)
            seats.booked = True
            seats.save()
        tickets = Tickets.objects.all().filter(user = request.user,seat__in = seat_lst)

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
        recent = True
        return render(request,'booking/paid.html',{'booked':tickets,'recent':recent})
    recent = False
    tickets = Tickets.objects.filter(user = request.user)
    return render(request,'booking/paid.html',{'booked':tickets,'recent':recent})
    
def paynow(request):
    if request.method == "POST":
        value_lst = request.POST['total']
        json_value = json.loads(value_lst)
        total = json_value[0]
        seats_number = json_value[1]
        venue_id = json_value[2][0]
        venue = Venue.objects.get(id=venue_id)
        seats = []
        gst =  total * 18//100
        discount = (total * 10//100)
        new_total = total + gst - discount
        for each in seats_number:
            seats.append(Seats.objects.get(number = each,venue = venue))
        context = {'venue':venue,'total':total,'seats':seats,'json_data':value_lst,'gst':gst,'discount':discount,'final':new_total}
    return render(request,'booking/paynow.html',context)


def favourites(request): 
     
     genre = [] 
     venue = []  
     for each in Tickets.objects.filter(user = request.user):
         genre.append(each.seat.venue.event.genre)
         venue.append(each.seat.venue.name)
     favourites = {}
     fav_venue = {}
     for each in genre:
         favourites.update({each:genre.count(each)})  
     for each in venue:
         fav_venue.update({each:genre.count(each)})  
     print(favourites)    
     fav = max(favourites,key= favourites.get)
     fav_v = max(fav_venue,key=fav_venue.get)
     suggestions = Event.objects.filter(genre = fav) 
     v_events = [] 
     for each in Venue.objects.filter(name = fav_v):
           v_events.append(Event.objects.get(name = each.event.name))
     return render(request,'booking/favourites.html',{'fav':fav,'fav_venue':fav_v,'venue':v_events,'suggestions':suggestions})

def about(request):
    return render(request,'booking/about.html')
         



