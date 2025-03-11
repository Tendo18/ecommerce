from django.shortcuts import get_object_or_404 
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from django.db import transaction
from django.urls import reverse
from django.conf import settings

from . serializers import *
from .models import*

# Create your views here.
#CATEGORY
class CategoryView(APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error : str(e)'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryDetailView(APIView):
    def get(self, request, id):
        try:
            category = get_object_or_404 (Category.objects.get(id=id))
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            category = get_object_or_404 (Category, id=id)
            serializer = CategorySerializer(isinstance=category, data=request.data, partial= True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"Error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
             return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            category = get_object_or_404 (Category, id=id)
            category.delete()
            return Response({"Message" :f" {category.title} deleted successfully" }, status=status.HTTP_200_OK  )
       
        except Exception as e:
             return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductView(APIView):
    def get(self, request):
        try:
            Products = Product.objects.all()
            serializer = CategorySerializer(Products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error : str(e)'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductDetailView(APIView):
    def get(self, request, id):
        try:
            product = get_object_or_404 (Product.objects.get(id=id))
            serializer = CategorySerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        try:
            product = get_object_or_404 (Product, id=id)
            serializer = ProductSerializer(instance=product, data=request.data, partial= True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"Error" : str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
             return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddToCartView(APIView):
    def post(self, request, id):
        try:
            #add product to cart
            product = get_object_or_404(Product, id=id)

            #cart id
            cart_id =  request.session.get('cart_id', None)

            while transaction.atomic():
                if cart_id:
                    cart = cart.objects.filter(id=cart_id).first()
                    if cart is None:
                        cart = Cart.objects.create(total=0)
                        request.session['cart_id'] = cart.id

                    #check if product in cart
                    product_in_cart =  cart.cartproduct_set.filter(product=product)
                    if product_in_cart:
                        cartproduct = product_in_cart
                    else:
                        cart = Cart.objects.create(total = 0)
                        request.session['cart_id'] = cart.id
                        cartproduct = CartProduct.objects.create(cart=cart, product=product, quantity=1, subtotal=product.price)
                        cartproduct.save()
                    #create a cart
                    cart = Cart.objects.create(total = 0)
                    request.session['cart_id'] = cart.id
                    cartproduct = CartProduct.objects.create(cart=cart, product=product, quantity=1, subtotal=product.price)
                    cartproduct.save()

                    #update the cart
                    cart.total += product.price
                    cart.save()
                    return Response({"Message" : "A new cart has been created"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#MY CART
class MyCartView(APIView):
    def get(self, request):
        try:
            cart_id = request.session.get('cart_id', None)
            if cart_id:
                cart = get_object_or_404(Cart, id=cart_id)

                #assign cart to user
                if request.user.is_authenticated and hasattr(request.user, 'profile'):
                    cart.profile = request.user.profile
                    cart.save()
                    cart.user = request.user
                serializer = CartSerializer(cart)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"Error" : "No cart found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#MANAGE CART
class ManageCartView(APIView):
    def post(self, request, id):
        action = request.data.get('action')
        try:
            cart_obj = get_object_or_404(CartProduct, id=id)
            cart = cart_obj.cart
            if action == "increase":
                cart_obj.quantity += 1
                cart_obj.subtotal += cart_obj.product.price
                cart_obj.save()
                cart.total += cart_obj.product.price
                cart.save()
                return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
            elif action == "decrease":
                cart_obj.quantity -= 1
                cart_obj.subtotal -= cart_obj.product.price
                cart_obj.save()
                if cart_obj.quantity == 0:
                    cart_obj.delete()
                return Response({"Message" : "Item decrease"}, status=status.HTTP_200_OK)
            elif action == "remove":
                cart.total -= cart_obj.subtotal
                cart.save()
                cart_obj.delete()
                return Response({"Message" : "Item removed"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
# CHECKOUT CART
class CheckoutCartView(APIView): 
    def post(self, request, id):
        try:
            cart_id = request.session.get('cart_id', None)
            if not cart_id:
                return Response({"Error" : "No cart found"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                cart_obj = get_object_or_404(Cart, id=cart_id)
            except Cart.DoesNotExist:
                return Response({"Error" : "Cart not found"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = CheckoutSerializer(data=request.data)
            if serializer.is_valid():
              order =  serializer.save(
                cart = cart_obj,
                amount = cart_obj.total,
                subtotal = cart_obj.total,
                order_status = "pending",
            )

            del request.session['cart_id']
            if order.payment_method == "paystack":
                payment_url = reverse('payment', args=[order.id])
                return Response({'redirect_url' : payment_url}, status=status.HTTP_200_OK)
            return Response({"Message" : "Order created successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        

# PAYMENT INITIALIZATION
class PaymentPageView(APIView):
    def get(self, request, id):
        try:
            order = get_object_or_404(Order, id=id)
        except Order.DoesNotExists:
            return Response({"Error" : "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        #CREATE PAYMENT REQUEST
        url = "https://api.paystack.co/transaction/initialize"
        headers = {"Authorization" : f"Bearer {self.PAYSTACK.KEY}"}
        data = {
            "amount" : order.amount * 100,
            "email" : order.email,
            "reference" : order.ref,
        }
        response = request.post(url, headers=headers, data=data)
        response_data = response.json()
        if response_data["status"]:
            paystack_url = response_data["data"]["authorization_url"]

            return Response({
                "order" : order.id,
                "total" : order.amount_value(),
                "paystack_public_key" : self.PAYSTACK['PUBLIC_KEY'],
                "paystack_url" : paystack_url,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"Error" : "Payment initialization failed"}, status=status.HTTP_400_BAD_REQUEST )


        
# VERIFY PAYMENT PAGE
class VerifyPaymentPageView(APIView):
    def get(self, request, id):
        try:
            order = get_object_or_404(Order, id=id)
            url = "https://api.paystack.co/transaction/initialize{ref}"
            headers = {"Authorization" : f"Bearer {self.PAYSTACK.KEY}"}
            response = request.post(url, headers=headers)
            response_data = response.json()
            if  response_data["status"] and response_data["data"]["status"] == "success":
                order.payment_complete = "completed"
                order.save()
                return Response({"Message" : "Payment successful"}, status=status.HTTP_200_OK)
            
            elif response_data["status"]["status"] == "abandoned":
                order.order_status = "pending"
                order.save()
                return Response({"Error" : "Payment failed or abandoned "}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({"Error" : "Payment failed"}, status=status.HTTP_200_OK)
            
        except Order.DoesNotExists:
            return Response({"Error" : "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"Error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        



