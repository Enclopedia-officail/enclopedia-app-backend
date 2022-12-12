from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'user'

urlpatterns = [
    path('/login', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # こちらを使用してtokenのリフレッシュを行う
    path('/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('/token/verify/', TokenVerifyView.as_view(), name="tokne_verify"),
    path('/create', views.AccountRegisterView.as_view(), name='profile_create'),
    path('/method', views.AccountRetrieveUpdateView.as_view(),
         name='account_method/'),
    path('/profile/',
         views.ProfileRetrieveUpdateView.as_view(), name='profile'),
    path('/adress/',
         views.AdressRetrieveUpdateView.as_view(), name='adress'),
    path('/register_confirm',
         views.AccountRegisterConfirmation.as_view(), name='confirmation'),
    path('/password/change', views.UserConfirmView.as_view(), name='confirm'),
    path('/sendgrid/contact', views.SendgridContactView.as_view(), name='sendgrid_contact'),
    path('/sendgrid/recipient', views.SendgridRecipient.as_view()),
    path('/sendgrid/suppressions/', views.SendgridSuppressionsView.as_view(), name='sendgrid_suppressions'),
    path('/email/subscribe', views.EmailSubscribeView.as_view(), name='email_subscribe'),
    path('/email_update', views.EmailUpdateView.as_view(), name='update_email'),
    path('/phone_number_update/', views.PhoneNumberUpdateAPIView.as_view()),
    path('/authenticate_phone_number/', views.AuthenticationNumberView.as_view())
]
