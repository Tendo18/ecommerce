from django.urls import path
from . import views


urlpatterns = [
    path('categories/', views.CategoryView.as_view()),
    path('category/<str:id>/', views.CategoryView.as_view()),
    path('products/', views.ProductView.as_view()),
    path('product/<str:id>/', views.ProductView.as_view()),
    path('addtocart/', views.AddToCartView.as_view()),
    path('mycart/', views.MyCartView.as_view()),
    path('managecart/<str:id>/', views.ManageCartView.as_view()),
    path('checkoutcart/<str:id>/', views.CheckoutCartView.as_view()),
    path('payment/<str:id>/', views.PaymentPageView.as_view(), name='payment'),
    path('/<str:ref>/', views.VerifyPaymentPageView.as_view(),),
]