from rest_framework import serializers

from ..models import Product, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "name", "user_type", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["sku", "name", "price", "description", "brand", "views", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:product-detail", "lookup_field": "sku"},
        }
