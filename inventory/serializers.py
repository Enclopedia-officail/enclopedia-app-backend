from rest_framework import serializers
from .models import Warehouse, Inventory
from product.serailizers import ProductSerializer

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'warehouse_name', 'postalcode', 'prefecture', 'region', 'address', 'building_name']

class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    warehouse = WarehouseSerializer(read_only=True)
    class Meta:
        model = Inventory
        fields = ['id', 'warehouse', 'classification', 'product', 'quantity']