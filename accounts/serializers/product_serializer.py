from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from accounts.models import Product, Order, OrderList

__all__ = ['ProductListSerializer', 'OrderProductSerializer', 'OrderDetailSerializer']


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'brand', 'price', 'image']
        # serializers.ListField(child=serializers.ImageField(allow_empty_file=True), write_only=True)


class ProductOrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderList
        fields = ["id", "category", "brand", "name", "price", "quantity", "image"]


class OrderDetailSerializer(serializers.ModelSerializer):

    products = ProductOrderListSerializer(source="order_list", many=True)

    class Meta:
        model = Order
        fields = ['id', 'insert_date', 'placed', 'total_price', 'total_quantity', 'products']

# class OrderProductSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Order
#         fields = ['product', 'quantity']
#
#     def validate(self, attrs):
#         """
#         This method will validate place and images credentials and also check user details.
#         :param attrs:
#         :return:
#         """
#         product = attrs.get('product')
#         quantity = attrs.get('quantity')
#
#         if not product:
#             raise ValidationError("Product doesn't exists")
#         # product = Product.objects.get(id=product, is_active=True)
#         if product.quantity < quantity:
#             raise ValidationError("At this quantity product is not available")
#
#         attrs['user'] = self.context['request'].user
#         return attrs


class OrderProductSerializer(serializers.ModelSerializer):
    products = serializers.ListField(child=serializers.IntegerField(allow_null=False), write_only=True)

    class Meta:
        model = Order
        fields = ['products', ]

    def validate(self, attrs):
        """
        This method will validate place and images credentials and also check user details.
        :param attrs:
        :return:
        """
        # products = attrs.get('products')
        # quantity = attrs.get('quantity')
        #
        # for product in products:
        #     if not Product.objects.filter(id=product, is_active=True):
        #         raise ValidationError("Product doesn't exists")
        #     product = Product.objects.get(id=product, is_active=True)
        #     if product.quantity < 1:
        #         raise ValidationError("At this quantity product is not available")

        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        products = validated_data.pop('products')
        validated_data['user'] = self.context['request'].user
        order = super().create(validated_data)
        price, quantity = 0, 0
        for product in products:
            if Product.objects.filter(id=product, is_active=True):
                product = Product.objects.get(id=product, is_active=True)
                order_list = OrderList(product=product, order=order)
                order_list.save()
                price += product.price
                quantity += 1
        order.total_price = price
        order.total_quantity = quantity
        order.save()

        return order
