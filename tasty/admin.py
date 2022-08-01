from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(OrderMeals)
admin.site.register(Delivery)
