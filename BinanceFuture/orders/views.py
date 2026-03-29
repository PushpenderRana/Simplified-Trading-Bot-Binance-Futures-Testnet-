from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, OrderSerializer
from .models import Orders

from binance.client import Client
from django.conf import settings


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class Registerview(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({'tokens': tokens, 'msg': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Loginview(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                tokens = get_tokens_for_user(user)
                return Response({'tokens': tokens, 'msg': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data

            try:
                client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET_KEY)
                if data['order_type'] == 'LIMIT':
                    order = client.futures_create_order(
                        symbol=data['symbol'],
                        side=data['side'],
                        type=data['order_type'],
                        price=str(data['price']),
                        quantity=str(data['quantity'])
                    )
                else:
                    order = client.futures_create_order(
                        symbol=data['symbol'],
                        side=data['side'],
                        type=data['order_type'],
                        quantity=str(data['quantity'])
                    )
            except Exception as e:
                return Response({'msg': 'Error occurred while creating order'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'msg': 'Order created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
