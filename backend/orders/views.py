from django.db import transaction
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .serializers import (
    AddToCartSerializer, CartSerializer, UpdateCartItemSerializer,
    OrderSerializer
)


def get_or_create_cart(user):
    """Helper — gets existing cart or creates one if user has none."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    """GET /api/orders/cart/ — returns the current user's cart with all items."""
    cart = get_or_create_cart(request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """
    POST /api/orders/cart/items/ — adds a product to cart.
    If the product is already in the cart, increments the quantity instead
    of creating a duplicate row (enforced by unique_together on the model).
    """
    serializer = AddToCartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    product_id = serializer.validated_data['product_id']
    quantity = serializer.validated_data['quantity']

    cart = get_or_create_cart(request.user)
    product = Product.objects.get(id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def cart_item_detail(request, pk):
    """
    PATCH /api/orders/cart/items/<id>/ — update quantity
    DELETE /api/orders/cart/items/<id>/ — remove item from cart
    """
    try:
        cart = get_or_create_cart(request.user)
        item = CartItem.objects.get(pk=pk, cart=cart)
    except CartItem.DoesNotExist:
        return Response({'detail': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = UpdateCartItemSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(CartSerializer(cart).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    """
    GET  /api/orders/ — list all orders for the current user
    POST /api/orders/ — place a new order from the current cart

    The POST is wrapped in a transaction so if anything fails
    (e.g. stock check), nothing is partially saved to the database.
    """
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
        return Response(OrderSerializer(orders, many=True).data)

    # POST — create order from cart
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.select_related('product').all()

    if not cart_items.exists():
        return Response({'detail': 'Your cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        # Calculate total from current product prices
        total = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(user=request.user, total_price=total)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price,  # snapshot price at checkout time
            )
            # Decrement stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear the cart after order is placed
        cart_items.delete()

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    """GET /api/orders/<id>/ — returns a single order (only if it belongs to the user)."""
    try:
        order = Order.objects.prefetch_related('items__product').get(pk=pk, user=request.user)
    except Order.DoesNotExist:
        return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(OrderSerializer(order).data)
