from django.contrib import admin

from api.models import Category, Order, OrderItem, Product, User

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderItem)
