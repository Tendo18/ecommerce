from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login, logout
from .serializers import*
from .models import*

# Create your views here.
#REGISTER USER
class RegisterUserView(APIView):
    def post(self, request):
        try:
            serializer = RegisterUserView(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#LOGIN USER        
class LoginUserView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({
                    "users": {"first_name":user.first_name},
                    "token": access_token}, status=status.HTTP_200_OK)
                return Response({"message": "Login successfully"}, status=status.HTTP_200_OK)
            return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#LOGOUT USER
class LogoutUserView(APIView):
    def post(self, request):
        try:
            logout(request)
            return Response({"Message": "Logout successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)     
    