import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import Category, Order, OrderItem, Product, User


class Command(BaseCommand):
    help = "Add sample application data."

    products = [
    # Electronics (5 products)
    {
        "name": "iPhone 15 Pro",
        "slug": "iphone-15-pro",
        "description": "Latest iPhone with A17 Pro chip, titanium design, and advanced camera system",
        "price": 999.99,
        "category": 1,
        "stock": 50,
        "image": "electronics/iphone15pro.jpg",
        "is_featured": False
    },
    {
        "name": "Samsung Galaxy S24 Ultra",
        "slug": "samsung-galaxy-s24-ultra",
        "description": "Premium Android smartphone with S Pen, 200MP camera, and Snapdragon 8 Gen 3",
        "price": 1199.99,
        "category": 1,
        "stock": 35,
        "image": "electronics/samsungs24ultra.jpg",
        "is_featured": False
    },
    {
        "name": "Sony WH-1000XM5 Headphones",
        "slug": "sony-wh-1000xm5-headphones",
        "description": "Industry-leading noise canceling wireless headphones with 30-hour battery",
        "price": 349.99,
        "category": 1,
        "stock": 75,
        "image": "electronics/sonyheadphones.jpg",
        "is_featured": False
    },
    {
        "name": "Apple Watch Series 9",
        "slug": "apple-watch-series-9",
        "description": "Advanced smartwatch with blood oxygen app, ECG, and Always-On Retina display",
        "price": 399.99,
        "category": 1,
        "stock": 60,
        "image": "electronics/applewatch9.jpg",
        "is_featured": False
    },
    {
        "name": "MacBook Air M3",
        "slug": "macbook-air-m3",
        "description": "Lightweight laptop with M3 chip, 15-inch Liquid Retina display, and 18-hour battery",
        "price": 1299.99,
        "category": 1,
        "stock": 40,
        "image": "electronics/macbookairm3.jpg",
        "is_featured": False
    },
    # Clothing (5 products)
    {
        "name": "Classic White Cotton T-Shirt",
        "slug": "classic-white-cotton-tshirt",
        "description": "100% cotton premium t-shirt with perfect fit and comfortable feel",
        "price": 24.99,
        "category": 2,
        "stock": 200,
        "image": "clothing/whitetshirt.jpg",
        "is_featured": False
    },
    {
        "name": "Slim Fit Denim Jeans",
        "slug": "slim-fit-denim-jeans",
        "description": "Comfortable stretch denim jeans with modern slim fit design",
        "price": 59.99,
        "category": 2,
        "stock": 150,
        "image": "clothing/denimjeans.jpg",
        "is_featured": False
    },
    {
        "name": "Waterproof Winter Jacket",
        "slug": "waterproof-winter-jacket",
        "description": "Insulated waterproof jacket with hood, perfect for cold and wet conditions",
        "price": 129.99,
        "category": 2,
        "stock": 80,
        "image": "clothing/winterjacket.jpg",
        "is_featured": False
    },
    {
        "name": "Cashmere Blend Sweater",
        "slug": "cashmere-blend-sweater",
        "description": "Luxurious cashmere and wool blend sweater for exceptional warmth and comfort",
        "price": 89.99,
        "category": 2,
        "stock": 100,
        "image": "clothing/cashmeresweater.jpg",
        "is_featured": False
    },
    {
        "name": "Yoga Leggings with Pockets",
        "slug": "yoga-leggings-with-pockets",
        "description": "High-waisted leggings with side pockets, perfect for workouts or casual wear",
        "price": 45.99,
        "category": 2,
        "stock": 120,
        "image": "clothing/yogaleggings.jpg",
        "is_featured": False
    },
    # Home & Kitchen (5 products)
    {
        "name": "Non-Stick Cookware Set",
        "slug": "non-stick-cookware-set",
        "description": "10-piece ceramic non-stick cookware set with dishwasher safe components",
        "price": 149.99,
        "category": 3,
        "stock": 65,
        "image": "home-kitchen/cookwareset.jpg",
        "is_featured": False
    },
    {
        "name": "Smart Coffee Maker",
        "slug": "smart-coffee-maker",
        "description": "WiFi enabled coffee maker with app control and scheduled brewing",
        "price": 129.99,
        "category": 3,
        "stock": 45,
        "image": "home-kitchen/coffeemaker.jpg",
        "is_featured": False
    },
    {
        "name": "Air Purifier with HEPA Filter",
        "slug": "air-purifier-with-hepa-filter",
        "description": "Quiet air purifier that removes 99.97% of dust, pollen, and airborne particles",
        "price": 199.99,
        "category": 3,
        "stock": 30,
        "image": "home-kitchen/airpurifier.jpg",
        "is_featured": False
    },
    {
        "name": "Memory Foam Bath Mat",
        "slug": "memory-foam-bath-mat",
        "description": "Super absorbent memory foam bath mat that dries quickly and feels luxurious",
        "price": 34.99,
        "category": 3,
        "stock": 90,
        "image": "home-kitchen/bathmat.jpg",
        "is_featured": False
    },
    {
        "name": "Stainless Steel Knife Set",
        "slug": "stainless-steel-knife-set",
        "description": "15-piece professional knife set with wooden block and sharpener",
        "price": 89.99,
        "category": 3,
        "stock": 55,
        "image": "home-kitchen/knifeset.jpg",
        "is_featured": False
    },
    # Books (5 products)
    {
        "name": "The Midnight Library",
        "slug": "the-midnight-library",
        "description": "Novel by Matt Haig about a library that contains books with different versions of one's life",
        "price": 16.99,
        "category": 4,
        "stock": 85,
        "image": "books/midnightlibrary.jpg",
        "is_featured": False
    },
    {
        "name": "Atomic Habits",
        "slug": "atomic-habits",
        "description": "James Clear's practical guide to building good habits and breaking bad ones",
        "price": 14.99,
        "category": 4,
        "stock": 120,
        "image": "books/atomichabits.jpg",
        "is_featured": False
    },
    {
        "name": "Python Crash Course, 3rd Edition",
        "slug": "python-crash-course-3rd",
        "description": "Hands-on introduction to programming with Python for beginners",
        "price": 39.99,
        "category": 4,
        "stock": 75,
        "image": "books/pythoncrashcourse.jpg",
        "is_featured": False
    },
    {
        "name": "The Hobbit",
        "slug": "the-hobbit",
        "description": "J.R.R. Tolkien's classic fantasy novel that precedes The Lord of the Rings",
        "price": 12.99,
        "category": 4,
        "stock": 200,
        "image": "books/thehobbit.jpg",
        "is_featured": False
    },
    {
        "name": "National Geographic World Atlas",
        "slug": "national-geographic-world-atlas",
        "description": "Comprehensive world atlas with detailed maps and geographical information",
        "price": 49.99,
        "category": 4,
        "stock": 40,
        "image": "books/worldatlas.jpg",
        "is_featured": False
    },
    # Sports & Outdoors (5 products)
    {
        "name": "Yoga Mat Premium",
        "slug": "yoga-mat-premium",
        "description": "Eco-friendly non-slip yoga mat with carrying strap and alignment markers",
        "price": 39.99,
        "category": 5,
        "stock": 110,
        "image": "sports-outdoors/yogamat.jpg",
        "is_featured": False
    },
    {
        "name": "Mountain Bike Helmet",
        "slug": "mountain-bike-helmet",
        "description": "Lightweight ventilated helmet with MIPS technology for enhanced protection",
        "price": 79.99,
        "category": 5,
        "stock": 60,
        "image": "sports-outdoors/bikehelmet.jpg",
        "is_featured": False
    },
    {
        "name": "Camping Tent 4-Person",
        "slug": "camping-tent-4-person",
        "description": "Weather-resistant dome tent with easy setup and rainfly",
        "price": 149.99,
        "category": 5,
        "stock": 35,
        "image": "sports-outdoors/campingtent.jpg",
        "is_featured": False
    },
    {
        "name": "Running Shoes",
        "slug": "running-shoes",
        "description": "Lightweight running shoes with cushioned midsole and breathable mesh",
        "price": 89.99,
        "category": 5,
        "stock": 95,
        "image": "sports-outdoors/runningshoes.jpg",
        "is_featured": False
    },
    {
        "name": "Portable Bluetooth Speaker",
        "slug": "portable-bluetooth-speaker",
        "description": "Waterproof wireless speaker with 24-hour battery life for outdoor adventures",
        "price": 119.99,
        "category": 5,
        "stock": 70,
        "image": "sports-outdoors/portablespeaker.jpg",
        "is_featured": False
    },
    # Beauty & Personal Care (5 products)
    {
        "name": "Vitamin C Serum",
        "slug": "vitamin-c-serum",
        "description": "Anti-aging facial serum with vitamin C, hyaluronic acid, and ferulic acid",
        "price": 29.99,
        "category": 6,
        "stock": 150,
        "image": "beauty-personal-care/vitamincserum.jpg",
        "is_featured": False
    },
    {
        "name": "Electric Toothbrush",
        "slug": "electric-toothbrush",
        "description": "Sonic electric toothbrush with multiple cleaning modes and pressure sensor",
        "price": 79.99,
        "category": 6,
        "stock": 85,
        "image": "beauty-personal-care/electrictoothbrush.jpg",
        "is_featured": False
    },
    {
        "name": "Hair Dryer Professional",
        "slug": "hair-dryer-professional",
        "description": "Ionic hair dryer with multiple heat/speed settings for fast drying",
        "price": 59.99,
        "category": 6,
        "stock": 65,
        "image": "beauty-personal-care/hairdryer.jpg",
        "is_featured": False
    },
    {
        "name": "Sunscreen SPF 50",
        "slug": "sunscreen-spf-50",
        "description": "Broad spectrum sunscreen that's water resistant and non-greasy",
        "price": 19.99,
        "category": 6,
        "stock": 200,
        "image": "beauty-personal-care/sunscreen.jpg",
        "is_featured": False
    },
    {
        "name": "Aromatherapy Essential Oil Set",
        "slug": "aromatherapy-essential-oil-set",
        "description": "Set of 6 premium essential oils with diffuser blends guide",
        "price": 34.99,
        "category": 6,
        "stock": 90,
        "image": "beauty-personal-care/essentialoils.jpg",
        "is_featured": False
    },
    # Toys & Games (5 products)
    {
        "name": "LEGO Classic Creative Brick Box",
        "slug": "lego-classic-creative-brick-box",
        "description": "790-piece LEGO set with bricks in 33 different colors for creative building",
        "price": 49.99,
        "category": 7,
        "stock": 75,
        "image": "toys-games/legobricks.jpg",
        "is_featured": False
    },
    {
        "name": "Board Game: Catan",
        "slug": "board-game-catan",
        "description": "Popular strategy game where players collect resources and build settlements",
        "price": 44.99,
        "category": 7,
        "stock": 60,
        "image": "toys-games/catan.jpg",
        "is_featured": False
    },
    {
        "name": "Remote Control Car",
        "slug": "remote-control-car",
        "description": "2.4GHz RC car with proportional steering and rechargeable battery",
        "price": 39.99,
        "category": 7,
        "stock": 85,
        "image": "toys-games/rccar.jpg",
        "is_featured": False
    },
    {
        "name": "Jigsaw Puzzle 1000 Pieces",
        "slug": "jigsaw-puzzle-1000-pieces",
        "description": "Landscape jigsaw puzzle with vibrant colors and challenging design",
        "price": 19.99,
        "category": 7,
        "stock": 110,
        "image": "toys-games/jigsawpuzzle.jpg",
        "is_featured": False
    },
    {
        "name": "Drone with HD Camera",
        "slug": "drone-with-hd-camera",
        "description": "Beginner-friendly drone with 720p camera and altitude hold function",
        "price": 79.99,
        "category": 7,
        "stock": 45,
        "image": "toys-games/drone.jpg",
        "is_featured": False
    },
    # Food & Grocery (5 products)
    {
        "name": "Extra Virgin Olive Oil",
        "slug": "extra-virgin-olive-oil",
        "description": "Premium cold-pressed olive oil from Mediterranean olives",
        "price": 24.99,
        "category": 8,
        "stock": 120,
        "image": "food-grocery/oliveoil.jpg",
        "is_featured": False
    },
    {
        "name": "Organic Coffee Beans",
        "slug": "organic-coffee-beans",
        "description": "Fair trade, organic Arabica coffee beans, medium roast",
        "price": 14.99,
        "category": 8,
        "stock": 95,
        "image": "food-grocery/coffeebeans.jpg",
        "is_featured": False
    },
    {
        "name": "Artisan Chocolate Assortment",
        "slug": "artisan-chocolate-assortment",
        "description": "Box of 16 handmade chocolates with various fillings and flavors",
        "price": 29.99,
        "category": 8,
        "stock": 70,
        "image": "food-grocery/chocolate.jpg",
        "is_featured": False
    },
    {
        "name": "Gourmet Popcorn Sampler",
        "slug": "gourmet-popcorn-sampler",
        "description": "Assorted flavors of premium popcorn: cheese, caramel, and butter",
        "price": 19.99,
        "category": 8,
        "stock": 150,
        "image": "food-grocery/popcorn.jpg",
        "is_featured": False
    },
    {
        "name": "Organic Honey",
        "slug": "organic-honey",
        "description": "Pure, raw honey from pesticide-free bee farms",
        "price": 12.99,
        "category": 8,
        "stock": 180,
        "image": "food-grocery/honey.jpg",
        "is_featured": False
    },
]

    categories = [
        {
            "name": "Electronics",
            "slug": "electronics",
            "description": "Latest gadgets and electronic devices",
        },
        {
            "name": "Clothing",
            "slug": "clothing",
            "description": "Fashionable clothes(All Ages)",
        },
        {
            "name": "Home & Kitchen",
            "slug": "home-kitchen",
            "description": "Everything for your home",
        },
        {
            "name": "Books",
            "slug": "books",
            "description": "Fiction, non-fiction, and educational books",
        },
        {
            "name": "Sports & Outdoors",
            "slug": "sports-outdoors",
            "description": "Equipment for sports and outdoor activities",
        },
        {
            "name": "Beauty & Personal Care",
            "slug": "beauty-personal-care",
            "description": "Products for personal grooming and wellness",
        },
        {
            "name": "Toys & Games",
            "slug": "toys-games",
            "description": "Fun for kids and adults alike",
        },
        {
            "name": "Food & Grocery",
            "slug": "food-grocery",
            "description": "Pantry staples and specialty foods",
        },
    ]

    featured_indices = random.sample(range(len(products)), 10)

    def handle(self, *args, **kwargs):
        # User.objects.create(
        #     email="erenyeager@mail.com",
        #     password="password",
        #     is_superuser=False,
        # )

        for cat in self.categories:
            Category(
                name=cat["name"],
                slug=cat["slug"],
                description=cat["description"]
            ).save()

        for (idx, prod) in enumerate(self.products):
            is_featured = False

            if idx in self.featured_indices:
                is_featured = True
            
            Product.objects.create(
                name=prod['name'],
                slug=prod['slug'],
                description=prod['description'],
                price=prod['price'],
                stock=prod['stock'],
                is_featured=is_featured,
                category=Category.objects.get(pk=prod['category'])
            )

        self.stdout.write(self.style.SUCCESS("Database population complete."))
