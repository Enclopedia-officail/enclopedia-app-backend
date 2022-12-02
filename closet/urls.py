from django.urls import path
from . import views

app_name = 'closet'

urlpatterns = [
    path('detail/<str:pk>', views.ClosetRetrieveUpdateDestroyView.as_view(), name='closet_edit'),
    path('create/', views.ClosetCreateView.as_view(), name='closet_create'),
    path('list/', views.ClosetListView.as_view(), name='closet_list'),
    path('cloth/basic', views.ClothBasicCreate.as_view(), name='cloth_basic_create'),
    path('cloth/premium', views.ClothPremiumCreate.as_view(), name='cloth_premium_create'),
    path('cloth/list/', views.ClothListView.as_view(), name='cloth_list'),
    path('cloth/<str:pk>', views.ClothDestroyView.as_view(), name='cloth_edit'),
    path('delete/', views.ClosetAllDeleteView.as_view(), name='closet_delete')
]
