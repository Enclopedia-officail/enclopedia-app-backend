from .models import Warehouse, Inventory
from rest_framework import generics
from rest_framework import Response
from .models import Warehouse, Inventory
from .serializers import WarehouseSerializer, InventorySerializer
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status

#在庫場所について
class WarehouseCreateView(generics.ListAPIView):
    pass

#warehouseで倉庫別のfilterにかけたり
class InventoryRetrieve(generics.RetrieveAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.select_related('warehouse', 'product').all()
    def get(self, request, pk):
        try:
            instance = get_object_or_404(Inventory, id=pk)
            serializer = self.serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

#全ての取得
class InventoryListAPIView(generics.ListAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.select_related('warehouse', 'product').all()
#倉庫ごとに取得
class InventoryFilterWarehouseView(generics.ListAPIView):
    def get(self, request):
        warehouse = request.GET['warehouse']
        instance = get_list_or_404(Inventory, warehouse_id=warehouse)
        serializer = self.serializer_class(instance, many=True, context={"request":request})
        return Response(serializer.data, status=status.HTTP_200_OK)


#productで取得