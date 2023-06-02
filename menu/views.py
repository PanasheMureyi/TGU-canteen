from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from menu.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.db.models import Q
from decimal import Decimal
from django.db import transaction
from django.db.models import Count





def menu(request):
    query = request.GET.get("q", "")
    restaurant = Restaurant.objects.first()
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    if query:
        menu_items = menu_items.filter(name__icontains=query)
    context = {'items': menu_items, 'query': query}
    return render(request, 'menu/menu.html', context)





def restaurant(request):
    restaurant = Restaurant.objects.all()
    menuitemsres = Restaurant.objects.first()
    #shows the items in order of highest reviews
    menuitems = MenuItem.objects.filter(restaurant=menuitemsres).annotate(review_count=Count('menureview')).order_by('-review_count')[:3]

    context = {"restaurants": restaurant, "menuitems": menuitems}
    return render(request, "menu/restaurant.html", context)





def order(request,order_id):
    items = MenuItem.objects.get(id=order_id)
    context = {'items': items}
    return render(request, 'menu/order.html', context)


@login_required
def add_to_cart(request, item_id):
    
    item = get_object_or_404(MenuItem, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        item=item,
        user=request.user,
        defaults={'quantity': quantity},
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
        
    return redirect('cart')

@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')




@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'menu/cart.html', {'cart_items': cart_items})

def login_view(request):
    """
    Displays the login page and logs the user in if the form is submitted.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('restaurant')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'menu/login.html')



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('restaurant')
    else:
        form = SignUpForm()
    return render(request, 'menu/register.html', {'form':form})


def logout_view(request):
    """
    Logs the user out and redirects to the login page.
    """
    logout(request)
    return redirect('restaurant')

def RestaurantReviews(request):
    restaurant=Restaurant.objects.get(id=1)
    reviews = RestaurantReview.objects.order_by('-created_at').all()
    context = {'reviews': reviews, 'restaurant': restaurant}
    

    return render(request, 'menu/reviews.html', context)

@login_required
def add_review(request):
    restaurant=Restaurant.objects.get(id=1)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = request.user
            review.save()
            form = ReviewForm() # clear form
        return redirect('reviews')
    else:
        form = ReviewForm()
    context = {'form': form}
    return render(request, 'menu/add_review.html',context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(RestaurantReview, pk=review_id)
    if request.user == review.user:
        review.delete()
        return redirect('reviews')
    else:
        return redirect('restaurant')

@login_required
@transaction.atomic
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        return redirect('restaurant')

    total_price = Decimal('0')
    order_items = []

    # Calculate total price and prepare order items
    for cart_item in cart_items:
        # Check if the item is in stock
        if cart_item.item.stock < cart_item.quantity:
            return render(request, 'menu/checkout_error.html', {'item': cart_item.item})

        total_price += cart_item.item.price * cart_item.quantity
        order_items.append(OrderItem(menu_item=cart_item.item, quantity=cart_item.quantity, price=cart_item.item.price))

    # Create an order and add the items to it
    restaurant = Restaurant.objects.get(pk=cart_items[0].item.restaurant.id)
    order = Order.objects.create(restaurant=restaurant, customer_name=request.user.username, customer_email=request.user.email, customer_phone='', total_price=total_price)

    for order_item in order_items:
        order_item.order = order  # Set the order field before saving
        order_item.save()

        # Decrease the stock of the item by the ordered quantity
        order_item.menu_item.stock -= order_item.quantity
        order_item.menu_item.save()

    # Clear the user's cart
    cart_items.delete()

    return render(request, 'menu/checkout_success.html', {'order': order})


