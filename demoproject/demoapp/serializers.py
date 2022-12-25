from rest_framework import serializers
from .models import ProductDetails

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetails
        # fields = ('product_name', 'image', )
        # exclude = ('product_price', )
        fields = '__all__'
 
