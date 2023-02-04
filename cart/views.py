from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem
from closet.models import Cloth

# Create your views here.

class CartCreateView(generics.CreateAPIView):
    queryset = Cart.objects.select_related('user').all()
    serializer_class = CartSerializer

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = self.serializer_class(cart)
            return Response(serializer.data)
        except:
            instance = Cart.objects.create(user=request.user)
            serializer = self.serializer_class(instance)
            return Response(serializer.data)

class CartRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Cart.objects.select_related('user').all()
    serializer_class = CartSerializer

    def get(self, request):
        cart = get_object_or_404(self.queryset, user=request.user)
        serializer = self.serializer_class(cart)
        return Response(serializer.data)

    def delete(self, request):

        cart = get_object_or_404(self.queryset, user=request.user)
        cart.delete()
        message = 'cartを削除しました'
        return Response(message, status=status.HTTP_200_OK)


# cartに商品を追加する
# user認証を受けている場合と受けていない場合に分けるようにする
class AddCartItem(generics.CreateAPIView):
    queserset = CartItem.objects.select_related('product', 'cart').all()
    serializer_class = CartItemSerializer

    # productのstock数を超えていればプラスできない
    # cart内に登録できる数の制御をするようにする
    def post(self, request):
        stock = request.data['stock']
        product_variation = []
        data = request.data

        if data.get('variation'):
            product_variation.append(data['variation'])

        cart_items = CartItem.objects.select_related('product', 'cart').filter(
            cart_id=data['cart'], product_id=data['product'])
        # 複数アイテムから重複がないかを調べれ個数をプラス、なければ作成
        if cart_items.exists():
            is_exist_product_list = []
            id = []
            for item in cart_items:
                exist_variation = item.variation.all()
                is_exist_product_list.append(list(exist_variation))
                id.append(item.id)
            if product_variation in is_exist_product_list or not is_exist_product_list:
                # productとvariationが一致した
                index = is_exist_product_list.index(product_variation)
                item_id = id[index]
                cart_item = CartItem.objects.select_related('product', 'cart').get(
                    product_id=request.data['product'], id=item_id)
                cart_item.quantite += int(request.data['quantite'])
                if int(stock) <= cart_item.quantite:
                    cart_item.quantite = int(stock)
                cart_item.save()
                cartitems = CartItem.objects.select_related(
                    'product', 'cart').filter(cart=request.data['cart'])
                serializer = self.serializer_class(
                    cartitems, many=True, context={"request":request})
                return Response(serializer.data)
            else:
                if data['quantite']:
                    quantity = int(data['quantite'])
                else:
                    quantity = 1
                cart_item = CartItem.objects.select_related('product', 'cart').create(
                    product_id=data['product'], cart=data.cart, quantite=quantity
                )
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                cart_item.save()
                cartitems = CartItem.objects.select_related(
                    'product', 'cart').filter(cart=request.data['cart'])
                serializer = self.serializer_class(
                    cartitems, many=True, context={"request":request})
                return Response(serializer.data)

        # product商品が追加されておらず新規作成をしなければならない状態
        else:
            quantity = int(request.data['quantite'])
            cart_item = CartItem.objects.select_related('product', 'cart').create(
                product_id=request.data['product'],
                cart_id=request.data['cart'],
                quantite=quantity
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
            cartitems = CartItem.objects.select_related(
                'cart', 'product').filter(cart=request.data['cart'])
            serializer = self.serializer_class(
                cartitems, many=True, context={"request":request})
        return Response(serializer.data)

# basicプランの場合はcartviewはこちらを使用する。


class CartItemAddBasicView(APIView):
    def post(self, request):
        product_variation = []
        data = request.data
        cart = data['cart']
        stock = data['stock']
        product = data['product']
        quantity = data['quantite']
        variation = data['variation']
        total_quantity = 0
        if variation:
            product_variation.append(variation)
        # cartアイテムがbasic内でレンタルできる数を超過していないか確認するための処理
        cart_items = CartItem.objects.select_related('product', 'cart').filter(
            cart_id=cart
        )
        # basicプランの場合はレンタル数は3つ
        try:
            # cartアイテム数が3つ以上ならerror
            if len(cart_items) < 3:
                for cart_item in cart_items:
                    total_quantity += cart_item.quantite
                # トータルで三つ以上の商品があった場合
                if total_quantity >= 3:
                    raise
            else:
                raise
            # cart item内に重複があった場合にはvariatioとvariationなしのアイテムの個数を調整する必要がある
            items = CartItem.objects.select_related('product', 'cart').filter(
                cart_id=cart, product_id=product)
            if items.exists():
                is_exist_product_variations_list = []
                id = []
                # variationの重複を確認
                for item in items:
                    exist_variations = item.variation.all()
                    is_exist_product_variations_list.append(
                        list(exist_variations))
                    id.append(item.id)
                if product_variation in is_exist_product_variations_list or not is_exist_product_variations_list:
                    index = is_exist_product_variations_list.index(
                        product_variation)
                    item_id = id[index]
                    cart_item = CartItem.objects.select_related('product', 'cart').get(
                        product_id=product, id=item_id
                    )
                    cart_item.quantite += int(request.data['quantite'])
                    if int(stock) <= cart_item.quantite:
                        cart_item.quantite = int(stock)
                    cart_item.save()

                    message = {'message': 'cartに商品を追加しました'}
                    return Response(message, status=status.HTTP_200_OK)
                # 新しくcartitemを作成する
                else:
                    CartItem.objects.select_related('product', 'cart').create(
                        product_id=product, cart_id=cart,  quantite=quantity
                    )
                    # variationを初期化するようにsルウ
                    if len(product_variation) > 0:
                        cart_item.variation.clear()
                        cart_item.variation.add(*product_variation)
                        cart_item.save()
                    message = {'message': 'cartに商品を追加しました'}
                    return Response(message, status=status.HTTP_200_OK)

            else:

                cart_item = CartItem.objects.select_related('product', 'cart').create(
                    product_id=product,
                    cart_id=cart,
                    quantite=quantity
                )
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                    cart_item.save()
                message = {'message': 'cartに商品を追加しました'}
                return Response(message, status=status.HTTP_200_OK)
        except:
            message = {'message': 'レンタルできる商品数は3着までです、カート内で予約を確定してください。'}
            return Response(message, status=status.HTTP_200_OK)

# premiumプランの場合のcartへの追加を制御する


class CartItemAddPremiumView(APIView):
    def post(self, request):
        product_variation = []
        data = request.data
        cart = data['cart']
        stock = data['stock']
        product = data['product']
        quantity = data['quantite']
        variation = data['variation']
        total_quantity = 0
        if variation:
            product_variation.append(variation)
        # cartアイテムがbasic内でレンタルできる数を超過していないか確認するための処理
        cart_items = CartItem.objects.select_related('product', 'cart').filter(
            cart_id=cart
        )
        # basicプランの場合はレンタル数は3つ
        try:
            # cartアイテム数が3つ以上ならerror
            if len(cart_items) < 4:
                for cart_item in cart_items:
                    total_quantity += cart_item.quantite
                # トータルで三つ以上の商品があった場合
                if total_quantity >= 4:
                    raise
            else:
                raise
            # cart item内に重複があった場合にはvariatioとvariationなしのアイテムの個数を調整する必要がある
            items = CartItem.objects.select_related('product', 'cart').filter(
                cart_id=data['cart'], product_id=data['product'])
            if items.exists():
                is_exist_product_variations_list = []
                id = []
                # variationの重複を確認
                for item in items:
                    exist_variations = item.variation.all()
                    is_exist_product_variations_list.append(
                        list(exist_variations))
                    id.append(item.id)
                if product_variation in is_exist_product_variations_list or not is_exist_product_variations_list:
                    index = is_exist_product_variations_list.index(
                        product_variation)
                    item_id = id[index]
                    cart_item = CartItem.objects.select_related('product', 'cart').get(
                        product_id=product, id=item_id
                    )
                    cart_item.quantite += int(request.data['quantite'])
                    if int(stock) <= cart_item.quantite:
                        cart_item.quantite = int(stock)
                    cart_item.save()
                    message = {'message': 'cartに商品を追加しました'}
                    return Response(message, status=status.HTTP_200_OK)
                # 新しくcartitemを作成する
                else:
                    print('point8')
                    CartItem.objects.select_related('product', 'cart').create(
                        product_id=product, cart_id=cart,  quantite=quantity
                    )
                    if len(product_variation) > 0:
                        cart_item.variation.clear()
                        cart_item.variation.add(*product_variation)
                    cart_item.save()
                    message = {'message': 'cartに商品を追加しました'}
                    return Response(message, status=status.HTTP_200_OK)
            else:
                cart_item = CartItem.objects.select_related('product', 'cart').create(
                    product_id=product,
                    cart_id=cart,
                    quantite=quantity
                )
                if len(product_variation) > 0:
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variation)
                    cart_item.save()
                message = {'message': 'cartに商品を追加しました'}
                return Response(message, status=status.HTTP_200_OK)
        except:
            message = {'message': 'レンタルできる商品数は4着までです、カート内で予約を確定してください。'}
            return Response(message, status=status.HTTP_200_OK)

# basicプランの場合のレンタルするproductの数の個数を変換する


class carItemBasicEdit(generics.UpdateAPIView):
    serializer_class = CartItemSerializer

    def update(self, request, *args, **kwargs):
        data = request.data
        cart = data['cart']
        quantity = data['quantite']
        product = data['product']
        total_quantity = 0
        update_item = []
        cart_items = CartItem.objects.select_related(
            'product', 'cart').filter(cart=cart)
        try:
            # cartアイテム数が3つ以上ならerror
            if len(cart_items) < 3:
                for cart_item in cart_items:
                    if cart_item.product_id == product:
                        update_item.append(cart_item)
                        cart_item.quantite = quantity
                    total_quantity += cart_item.quantite
                # トータルで三つ以上の商品があった場合
                if total_quantity >= 3:
                    raise
                update_item[0].save()
                serializer = self.serializer_class(
                    cart_items, many=True, context={"request": request})
                return Response(serializer.data)
            else:
                raise
        except:
            message = {'message': 'レンタルできる個数が超過してします。'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class carItemPremiumEdit(generics.UpdateAPIView):
    serializer_class = CartItemSerializer

    def update(self, request, *args, **kwargs):
        data = request.data
        cart = data['cart']
        quantity = data['quantite']
        product = data['product']
        total_quantity = 0
        update_item = []
        cart_items = CartItem.objects.select_related(
            'product', 'cart').filter(cart=cart)
        try:
            # cartアイテム数が3つ以上ならerror
            if len(cart_items) < 4:
                for cart_item in cart_items:
                    if cart_item.product_id == product:
                        update_item.append(cart_item)
                        cart_item.quantite = quantity
                    total_quantity += cart_item.quantite
                # トータルで三つ以上の商品があった場合
                if total_quantity >= 4:
                    raise
                update_item[0].save()
                serializer = self.serializer_class(
                    cart_items, many=True, context={"request":request})
                return Response(serializer.data)
            else:
                raise

        except:
            message = {'message': 'レンタルできる個数が超過してします。'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class CartItemEdit(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.select_related('product', 'cart').all()
    serializer_class = CartItemSerializer
    # userのcartのアイテム一覧を取得する

    # cartはqueryから取得するようにする
    def get(self, request):
        cart_item = get_list_or_404(
            self.queryset, cart_id=request.GET['cart'])
        serializer = self.serializer_class(
            cart_item, many=True, context={"request":request})
        return Response(serializer.data)
    # cartアイテムの数の変更or削除を実行するためのview

    # プラン別にカート内の登録できる数を制御する必要がある。
    def update(self, request, *args, **kwargs):
        instance = CartItem.objects.get(
            product_id=request.data['product'], cart_id=request.data['cart'])
        instance.quantite = request.data['quantity']
        instance.save()
        cart_item = get_list_or_404(
            self.queryset, cart_id=request.data['cart'])
        serializer = self.serializer_class(
            cart_item, many=True)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = CartItem.objects.get(
            product_id=request.GET['product'], cart_id=request.GET['cart'])
        instance.delete()
        cart_item = get_list_or_404(
            self.queryset, cart_id=request.GET['cart'])
        serializer = self.serializer_class(
            cart_item, many=True, context={"request":request})
        return Response(serializer.data)

#closet内商品をまとめて予約する

class AddClosetItemView(APIView):
    def post(self, request):
        try:
            closet_id = request.data['closet_id']
            cart_id = request.data['cart_id']
            clothes = Cloth.objects.filter(closet_id=closet_id)
            cartitems = CartItem.objects.filter(cart_id=cart_id)
            if len(cartitems) > 0:
                cartitems.delete()

            cloth_list = []
            for cloth in clothes:
                cloth_list.append(CartItem(product=cloth.product, quantite=1, cart_id=cart_id))
            CartItem.objects.bulk_create(cloth_list)

            message={"message":"カート内にアイテムを追加しました"}
            return Response(message, status=status.HTTP_201_CREATED)
        except:
            message="商品の追加に失敗しました"
            return Response(message, status=status.HTTP_400_BAD_REQUEST)