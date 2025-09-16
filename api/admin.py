from django.contrib import admin

from api.models import Category, Order, OrderItem, Product

admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(User)
admin.site.register(Order)
admin.site.register(OrderItem)
