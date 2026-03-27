from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_detail, name='cart-detail'),
    path('cart/items/', views.add_to_cart, name='cart-add'),
    path('cart/items/<int:pk>/', views.cart_item_detail, name='cart-item-detail'),
    path('', views.order_list_create, name='order-list-create'),
    path('<int:pk>/', views.order_detail, name='order-detail'),
]
