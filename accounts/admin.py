from django.contrib import admin

from .models import Product, Order, OrderList

from django.contrib.auth import get_user_model

User = get_user_model()


class OrderListInline(admin.TabularInline):
    model = OrderList


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderListInline, ]


# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderList)
