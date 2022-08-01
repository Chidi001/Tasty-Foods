from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractUser
from django.forms import BooleanField, UUIDField

# Create your models here.



class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=False)
    email = models.CharField(max_length=200,null=True)
    device_key = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True) 

    def __str__(self):
        if self.name:
            name = self.name
        else:
            name = self.device_key
        return str(name)

class Category(models.Model):
    category_id = models.CharField(max_length=60,null=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField()
   
    def __str__(self):
        return self.name

class Menu(models.Model):
    Meal = models.CharField(max_length=100,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET('Unspecified'))
    image = models.ImageField(null=True,blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=7,decimal_places=2)
    active = models.BooleanField(default=True,null=True,blank=True)
   
    def __str__(self):
        return self.Meal

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url



class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100,null=True)
   
    def __str__(self):
        return str(self.order_id)
    
    @property
    def get_cart_total(self):
        ordermeals = self.ordermeals_set.all()
        total =sum([meal.get_total for meal in ordermeals])
        return total

    @property
    def get_cart_meals(self):
        ordermeals = self.ordermeals_set.all()
        total =sum([meal.quantity for meal in ordermeals])
        return total

  

    

class Delivery(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    address = models.CharField(max_length=100,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    state = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    zipcode =models.CharField(max_length=100,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address

class OrderMeals(models.Model):
    meal =models.ForeignKey(Menu,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date =  models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
    
        total = self.meal.price * self.quantity
        return total



  
    
    