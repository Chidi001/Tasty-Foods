from unicodedata import category
from django.shortcuts import render,redirect
from tasty.forms import MyUserCreationForm
from django.contrib.auth.models import User
from tasty.utils import guestuser
from .models import *
import datetime
from django.db.models import Q
from django.http import JsonResponse
import json
import uuid
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.



def loginpage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('menu')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('menu')
        else:
            messages.error(request,'User email or password is invalid')

    context = {'page':page}
    return render (request,'base/login_register.html',context)




def home(request):
    
   
    if request.user.is_authenticated:
        
        q = request.GET.get('q') if request.GET.get('q') !=None else ''

        foods = Category.objects.filter(Q(name__icontains=q)|Q(description__icontains=q)
        |Q(category_id__icontains=q))
        meals = Menu.objects.filter(Q(Meal__icontains=q)| 
        Q(category__name__icontains=q)
        |Q(image__icontains=q)|Q(description__icontains=q)
        |Q(price__icontains=q)|Q(active__icontains=q)|Q())
        customer = request.user.customer
        order,create = Order.objects.get_or_create(customer=customer,complete=False)
        cartitems = order.get_cart_meals
    else:
        data = guestuser(request)
        customer =data['customer']
        q = request.GET.get('q') if request.GET.get('q') !=None else ''

        foods = Category.objects.filter(Q(name__icontains=q)|Q(description__icontains=q)
        |Q(category_id__icontains=q))
        meals = Menu.objects.filter(Q(Meal__icontains=q)| 
        Q(category__name__icontains=q)
        |Q(image__icontains=q)|Q(description__icontains=q)
        |Q(price__icontains=q)|Q(active__icontains=q)|Q())
        order,create = Order.objects.get_or_create(customer=customer,complete=False)
        cartitems = order.get_cart_meals

    context = {'meals':meals,'foods':foods,'cartitems':cartitems}
    return render(request,'base/menu.html',context)

def cart(request):
    if request.user.is_authenticated:   
        customer = request.user.customer
        order,create = Order.objects.get_or_create(customer=customer,complete=False)
        items =order.ordermeals_set.all()
        cartitems = order.get_cart_meals

    else:
        data = guestuser(request)
        customer =data['customer']
        order,create = Order.objects.get_or_create(customer=customer,complete=False)
        items =order.ordermeals_set.all()
        cartitems = order.get_cart_meals
        

    context ={'order':order,'items':items,'cartitems':cartitems}
    return render(request,'base/cart.html',context)


def cartupdate(request):
    data = json.loads(request.body.decode("utf-8"))
    mealId = data['mealId']
    action = data['action']
    print ('meal :',mealId)
    if request.user.is_authenticated:
        customer = request.user.customer
        
    else:
        data = guestuser(request)
        customer =data['customer']
    
    meal = Menu.objects.get(id=mealId)
    order,create = Order.objects.get_or_create(customer=customer,complete=False)
    ordermeals,create = OrderMeals.objects.get_or_create(order=order,meal=meal)
    items = order.ordermeals_set.all()
    cartitems = order.get_cart_meals

    if action == 'add':
        ordermeals.quantity = (ordermeals.quantity + 1)
    elif action == 'remove':
        ordermeals.quantity = (ordermeals.quantity - 1)

    ordermeals.save()

    if ordermeals.quantity <= 0:
        ordermeals.delete()


    return JsonResponse('data complete',safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        

    else:
        data = guestuser(request)
        customer =data['customer']
        
    order,create = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.ordermeals_set.all()
    cartitems =order.get_cart_meals


    context = {'order':order,'items':items,'cartitems':cartitems}
    return render(request,'base/checkout.html',context)


def processorder(request):
    order_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    total = float(data['userInfoData']['total'])
    
    if request.user.is_authenticated:
        customer = request.user.customer
        
        order,create = Order.objects.get_or_create(customer=customer,complete=False)
        order.order_id = order_id

        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        delivery = Delivery.objects.create(
            customer = customer,
            order = order,
            address = data['deliveryInfo']['address'],
            state = data['deliveryInfo']['state'],
            city = data['deliveryInfo']['city'],
            zipcode = data['deliveryInfo']['zipcode'],
        )
    else:
        customer=Customer.objects.get(device_key= request.session['anony'])
        customer.name = data['userInfoData']['name'],
        customer.email = data['userInfoData']['name']
        
        
        customer.save()
        order,create = Order.objects.get_or_create(customer=customer,complete=False)
        order.order_id = order_id
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()

        delivery = Delivery.objects.create(
            customer = customer,
            order = order,
            address = data['deliveryInfo']['address'],
            state = data['deliveryInfo']['state'],
            city = data['deliveryInfo']['city'],
            zipcode = data['deliveryInfo']['zipcode'],
        )
        

    
    return JsonResponse('Payment complete',safe=False)

def logoutUser(request):
    logout(request)
    return redirect('menu')


def registerUser(request):
    form = MyUserCreationForm
    if request.method =='POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            customer = Customer.objects.create(
                user = user,
                name = user.username,
                email = user.email
            )
        
            
            login(request,user)
            return redirect('menu')
    else:

        messages.error(request,'User email or password is invalid')
    context = {'form':form}
    return render(request,'base/login_register.html', context)






    
   
