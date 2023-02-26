from django.urls import path
from .import views
urlpatterns = [
    path('login', views.login_, name='login'),
    path('logout', views.logout_, name='logout'),
    path('seats<int:id>',views.display_seats,name = 'seats'),
    path('seat-number/<int:id>/<int:id2>', views.choose_seats, name = 'choose'),
    path('paid', views.booked, name ='booked'),
    path('movies', views.movies, name = 'movies'),
    path('venues<int:id>', views.venues, name = 'venues')
]