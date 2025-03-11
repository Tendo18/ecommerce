from rest_framework import serializers
from .models import *

#CATEGORY SERIALIZERS
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

#PRODUCT SERIALIZERS
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

#CART SERIALIZERS
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

#CART PRODUCT SERIALIZERS
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = '__all__'

#ORDER SERIALIZERS
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

##CHECKOUT SERIALIZERS
class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        models = Order
        exclude = ['order', 'amount', 'order status', 'subtotal', 'payment complete', 'ref']

        
