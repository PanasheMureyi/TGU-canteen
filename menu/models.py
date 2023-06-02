from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='restaurant_images', blank=True, null=True)  # New image field
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New fields for reviews
    avg_rating = models.FloatField(default=0)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def calculate_avg_rating(self):
        reviews = RestaurantReview.objects.filter(restaurant=self)
        if reviews.exists():
            self.avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        else:
            self.avg_rating = 0
        self.save()


from django.db import models
from django.utils import timezone
from django.db.models import Avg

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='menu_item_images', blank=True, null=True)  # New image field
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # New fields for reviews
    avg_rating = models.FloatField(default=0)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def calculate_avg_rating(self):
        reviews = MenuReview.objects.filter(menu=self)
        if reviews.exists():
            self.avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        else:
            self.avg_rating = 0
        self.save()



class MenuReview(models.Model):
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    customer_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"OrderItem #{self.id} ({self.menu_item.name})"


class CartItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
