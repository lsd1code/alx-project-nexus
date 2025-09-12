from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import Category, Order, OrderItem, Product


class Command(BaseCommand):
    help = "Add sample application data."

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

    def handle(self, *args, **kwargs):
        for cat in self.categories:
            print(cat["name"])

        self.stdout.write(self.style.SUCCESS("Database population complete."))
