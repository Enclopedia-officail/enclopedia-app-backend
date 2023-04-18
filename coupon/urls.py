from django.urls import path
from . import views

app_name = 'coupon'

urlpatterns = [
    path('discount', views.CouponDiscountView.as_view(), name='discount_price'),
    path('utilised/', views.UtilisedCouponView.as_view(), name='utilised_coupon'),
    path('invitation/', views.InvitationView.as_view(), name='invitation_coupon'),
    path('code/', views.InvitationCodeGetView.as_view(), name='get_invitation_code'),
    path('invtion_code/validation/', views.InvitationCodeValidateView.as_view(), name='invitation_code_validation'),
    path('issuing_list/', views.IssuingListView.as_view(), name='issuing_list')
]