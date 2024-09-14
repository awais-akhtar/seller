from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.contrib import admin

urlpatterns = [
    path('', index, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    #  application 
    path('Likeediamonds/', Likeediamonds, name='Likeediamonds'),
    path('tiktokcoins/', tiktokcoins, name='tiktokcoins'),
    # tiktok
    path('gettiktokiddata/', gettiktokiddata, name='gettiktokiddata'),
    #likee
    path('getlikeeiddata/', getlikeeiddata, name='getlikeeiddata'),  # recieving profile data
    # invoices
    path('tiktokinvoice/', tiktokinvoice, name='tiktokinvoice'),
    path('likeeinvoice/', likeeinvoice, name='likeeinvoice'), # for billing invoice 
    # status
    path('tracking/', tracking, name='tracking'), #
    # sucessdiamonds/coins
    path('sucessdiamonds/', sucessdiamonds, name='sucessdiamonds'), # for sucessdiamonds
    path('sucesscoins/', sucesscoins, name='sucesscoins'), # for sucesscoins
]
