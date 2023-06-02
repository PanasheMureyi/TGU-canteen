from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(RestaurantReview)
admin.site.register(MenuReview)

