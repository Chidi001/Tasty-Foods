from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='menu'),
    path('cart/',views.cart,name='cart'),
    path('updatemenu/',views.cartupdate,name="updatemenu"),
    
    path('checkout/',views.checkout,name="checkout"),
    path('process_payment/',views.processorder,name="process_payment"),

    path('login/',views.loginpage,name="login"),
     path('register/',views.registerUser,name="register"),
      path('logout/',views.logoutUser,name="logout"),


]