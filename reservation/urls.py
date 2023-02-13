from django.urls import path
from . import views

app_name = 'reservation'

urlpatterns = [
    path('<uuid:pk>',views.ReservationGetView.as_view()),
    path('item/', views.ReservationCreateView.as_view(), name='reservation'),
    path('item/<uuid:pk>', views.GetReservationItemView.as_view(), name='get_reservation_item'),
    path('list/', views.ReservationListItemView.as_view(), name="reservation_list"),
    path('latest', views.ReservationLatestDataView.as_view(), name="reservation_latest_data"),
    path('rental/', views.ReservationRentalListView.as_view(), name="reservation_rental"),
    path('rental/half_year/', views.ReservationRentalHalfYearView.as_view(), name="reservation_rental_half_year"),
    path('items/', views.ReservationItemView.as_view(), name='reservation_item'),
    path('shipping/<uuid:pk>', views.ShippingNumberUpdateView.as_view()),
    path('return_shipping/<uuid:pk>', views.ReturnShippingNumberUpdateView.as_view()),
    path('return_product_confirm/<uuid:pk>', views.ReturnProductConfirmView.as_view()),
    path('rental/product/confirm/', views.ReservationItemUserGet.as_view(), name='reservation_confirm'),
    path('shipping_list/', views.ShippingReservationsListView.as_view(), name='shipping_list'),
    path('complete_return/<uuid:pk>', views.CompleteRetrunView.as_view(), name='complete_return'),
    path('item/<uuid:pk>/review', views.UpdateReservationItemReviewView.as_view(), name='update_review'),
]
