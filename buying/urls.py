from django.urls import path
from . import views

app_name = 'buying'

urlpatterns = [
    path('', views.BuyingReservationItemView.as_view(), name='buying'),
    path('order_item_list', views.OrderItemListView.as_view(), name='order_item_list'),
    path('order_item', views.OrderItemCreateView.as_view(), name='order_item'),
    path('order_item/<str:pk>', views.OrderItemGetView.as_view()),
    path('order', views.OrderCreateView.as_view(), name='order'),
    path('payment', views.PaymentCreateView.as_view(), name='payment'),
]