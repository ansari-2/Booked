from django.urls import path
from .import views
urlpatterns = [
    path('login', views.login_, name='login'),
    path('logout', views.logout_, name='logout'),
    path('seats<int:id>',views.display_seats,name = 'seats'),
    path('seat-number/<int:id>/<int:id2>', views.choose_seats, name = 'choose'),
    path('venues<int:id>', views.venues, name = 'venues'),
    path('main', views.main, name = 'main'),
    path('explore<int:id>', views.explore, name = 'explore'),
    path('search', views.search_bar, name = 'search_bar'),
    path('user',views.display, name = 'display'),
    path('create',views.userProfile, name = 'profile'),
    path('submit', views.submit,name = 'submit'),
    path('test',views.test_total,name='test'),
    path('slider',views.display_slider, name='slider')
]

# path('paid', views.booked, name ='booked'),