from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('item/', views.ReservationCreateView.as_view(), name='reservation'),
    path('list/', views.ReservationListItemView.as_view(), name="resrvation"),
    path('latest', views.ReservationLatestDataView.as_view(), name="reservation_latest_data"),
    path('rental/', views.ReservationRentalListView.as_view(), name="reservation_rental"),
    path('rental/half_year/', views.ReservationRentalHalfYearView.as_view(), name="reservation_rental_half_year"),
    path('items/', views.ReservationItemView.as_view(), name='reservation_item'),
    path('shipping/<uuid:pk>', views.ShippingNumberUpdateView.as_view()),
    path('return_shipping/<uuid:pk>', views.ReturnShippingNumberUpdateView.as_view()),
    path('return_product_confirm/<uuid:pk>', views.ReturnProductConfirmView.as_view()),
    path('rental/product/confirm/', views.ReservationItemUserGet.as_view(), name='reservation_confirm')
]
