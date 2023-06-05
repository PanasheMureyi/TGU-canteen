from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('', views.restaurant, name='restaurant'),
    #path('order/', views.order, name='order'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('order/<int:order_id>/', views.order, name='order'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('register/', views.register, name='register'),
     path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('reviews/', views.RestaurantReviews, name='reviews'),
    path('add-review',views.add_review,name='add-review'),
    path('delete-review/<int:review_id>/',views.delete_review,name='delete-review'),
    #path('product/<int:product_id>/', views.product,name='product'),
     path('product/<int:product_id>/', views.product_detail, name='product'),
    # path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('view-cart/', views.view_cart, name='view_cart'),
    
    # path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
]
