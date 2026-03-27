from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product
from orders.models import Cart, CartItem, Order, OrderItem
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # --- Categories ---
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics'},
            {'name': 'Clothing', 'slug': 'clothing'},
            {'name': 'Books', 'slug': 'books'},
            {'name': 'Home & Kitchen', 'slug': 'home-kitchen'},
            {'name': 'Sports', 'slug': 'sports'},
        ]
        categories = []
        for data in categories_data:
            cat, _ = Category.objects.get_or_create(slug=data['slug'], defaults={'name': data['name']})
            categories.append(cat)
        self.stdout.write(f'  Created {len(categories)} categories')

        # --- Products ---
        products_data = [
            {'name': 'Wireless Headphones', 'description': 'Noise cancelling over-ear headphones with 30hr battery.', 'price': '89.99', 'stock': 50, 'category': 'electronics'},
            {'name': 'Mechanical Keyboard', 'description': 'TKL mechanical keyboard with RGB backlight.', 'price': '129.99', 'stock': 30, 'category': 'electronics'},
            {'name': 'USB-C Hub', 'description': '7-in-1 USB-C hub with HDMI, USB 3.0, and SD card slots.', 'price': '39.99', 'stock': 75, 'category': 'electronics'},
            {'name': 'Smartphone Stand', 'description': 'Adjustable aluminium desk stand for phones and tablets.', 'price': '19.99', 'stock': 100, 'category': 'electronics'},
            {'name': 'Classic White T-Shirt', 'description': '100% cotton unisex t-shirt. Available in all sizes.', 'price': '14.99', 'stock': 200, 'category': 'clothing'},
            {'name': 'Slim Fit Jeans', 'description': 'Stretch denim slim fit jeans in dark blue.', 'price': '49.99', 'stock': 80, 'category': 'clothing'},
            {'name': 'Hooded Sweatshirt', 'description': 'Fleece-lined pullover hoodie. Warm and comfortable.', 'price': '34.99', 'stock': 60, 'category': 'clothing'},
            {'name': 'Running Sneakers', 'description': 'Lightweight mesh running shoes with cushioned sole.', 'price': '74.99', 'stock': 45, 'category': 'clothing'},
            {'name': 'Clean Code', 'description': 'A handbook of agile software craftsmanship by Robert C. Martin.', 'price': '29.99', 'stock': 40, 'category': 'books'},
            {'name': 'The Pragmatic Programmer', 'description': 'Your journey to mastery, 20th anniversary edition.', 'price': '34.99', 'stock': 35, 'category': 'books'},
            {'name': 'Atomic Habits', 'description': 'An easy and proven way to build good habits by James Clear.', 'price': '16.99', 'stock': 90, 'category': 'books'},
            {'name': 'Non-Stick Frying Pan', 'description': '28cm non-stick frying pan with heat-resistant handle.', 'price': '24.99', 'stock': 55, 'category': 'home-kitchen'},
            {'name': 'Coffee Maker', 'description': '12-cup programmable drip coffee maker with thermal carafe.', 'price': '59.99', 'stock': 25, 'category': 'home-kitchen'},
            {'name': 'Yoga Mat', 'description': 'Non-slip 6mm thick yoga mat with carrying strap.', 'price': '27.99', 'stock': 70, 'category': 'sports'},
            {'name': 'Resistance Bands Set', 'description': 'Set of 5 resistance bands for home workouts.', 'price': '18.99', 'stock': 120, 'category': 'sports'},
        ]
        category_map = {c.slug: c for c in categories}
        products = []
        for data in products_data:
            cat = category_map[data['category']]
            product, _ = Product.objects.get_or_create(
                name=data['name'],
                defaults={
                    'description': data['description'],
                    'price': Decimal(data['price']),
                    'stock': data['stock'],
                    'category': cat,
                }
            )
            products.append(product)
        self.stdout.write(f'  Created {len(products)} products')

        # --- Users ---
        users_data = [
            {'email': 'alice@example.com', 'username': 'alice', 'first_name': 'Alice', 'last_name': 'Smith', 'password': 'password123'},
            {'email': 'bob@example.com', 'username': 'bob', 'first_name': 'Bob', 'last_name': 'Jones', 'password': 'password123'},
            {'email': 'carol@example.com', 'username': 'carol', 'first_name': 'Carol', 'last_name': 'White', 'password': 'password123'},
        ]
        users = []
        for data in users_data:
            if not User.objects.filter(email=data['email']).exists():
                user = User.objects.create_user(**data)
                users.append(user)
            else:
                users.append(User.objects.get(email=data['email']))
        self.stdout.write(f'  Created {len(users)} users')

        # --- Carts with items ---
        for user in users:
            cart, _ = Cart.objects.get_or_create(user=user)
            # Add 2 random products to each user's cart
            for product in random.sample(products, 2):
                CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': random.randint(1, 3)}
                )
        self.stdout.write(f'  Created carts for {len(users)} users')

        # --- Orders ---
        for user in users:
            # Create 2 past orders per user
            for _ in range(2):
                order_products = random.sample(products, random.randint(1, 3))
                total = sum(p.price * random.randint(1, 2) for p in order_products)
                order = Order.objects.create(
                    user=user,
                    status=random.choice(['pending', 'processing', 'shipped', 'delivered']),
                    total_price=total,
                )
                for product in order_products:
                    qty = random.randint(1, 2)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=qty,
                        unit_price=product.price,
                    )
        self.stdout.write(f'  Created 2 orders per user')

        self.stdout.write(self.style.SUCCESS('Done! Database seeded successfully.'))
