from django.urls import path
from . import views

app_name = 'buying'

urlpatterns = [
    path('', views.BuyingReservationItemView.as_view())
]