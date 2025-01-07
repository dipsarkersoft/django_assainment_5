from django.contrib import admin
from django.urls import path
from .views import editProfile,UserLogoutView,AllOrderView,UserLoginView,UserRegistrationView,DepositMoneyView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   path('register/',UserRegistrationView.as_view(),name='register'),
   path('profile/order',AllOrderView.as_view(),name='allorder'),
   path('profile/',editProfile,name='profile'),
   path('deposit/',DepositMoneyView.as_view(),name='deposit'),
   path('logout/',UserLogoutView.as_view(),name='logout'),
   path('login/',UserLoginView.as_view(),name='login'),
    
]
