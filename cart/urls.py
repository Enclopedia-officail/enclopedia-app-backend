from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('create/', views.CartCreateView.as_view(), name="cart_create"),
    path('edit/', views.CartRetrieveDestroyView.as_view(), name="cart_edit"),
    path('cartitem/', views.AddCartItem.as_view(), name='cartitem'),
    path('cartitem/basic/create',
         views.CartItemAddBasicView.as_view(), name="cartitem_basic"),
    path('cartitem/premium/create',
         views.CartItemAddPremiumView.as_view(), name="cartitem_premium"),
    path('cartitem/edit/', views.CartItemEdit.as_view(), name='cartitem_edit'),
    path('closet', views.AddClosetItemView.as_view(), name="closet_cart")
]
