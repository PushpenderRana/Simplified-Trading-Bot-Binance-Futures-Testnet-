from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Orders

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs
    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

class OrderSerializer(serializers.Serializer):
    class Meta:
        model = Orders
        fields = ['symbol', 'order_type', 'side', 'price', 'quantity']
    
    def validate(self, attrs):
        order_type = attrs.get('order_type')
        price = attrs.get('price')
        quantity = attrs.get('quantity')
        if order_type == 'LIMIT' and price is None:
            raise serializers.ValidationError("Price is required for LIMIT orders")
        if quantity is None:
            raise serializers.ValidationError("Quantity is required")
        if price is not None and price <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return attrs