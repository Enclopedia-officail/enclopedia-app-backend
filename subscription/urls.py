from django.contrib.auth import views
from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'subscription'

urlpatterns = [
    path('account', views.StripeAccountView.as_view()),
    path('subscription/user_info',
         views.StripeUserInfoView.as_view(), name="stripe_user_info"),
    path('subscription/config/',
         views.StripeConfigView.as_view(), name='config'),
    path('subscription/payment/', views.StripeCustomerView.as_view(), name='payment'),
    path('subscription/invoice/upcoming', views.StripeUpcomingInvoice.as_view(), name='payment_upcoming'),
    path('secret_info/', views.CreditInfoView.as_view(), name='secret_info'),
    path('checkout/', views.StripeCheckoutView.as_view(), name='checkout'),
    path('webhook/', views.webhook_view, name='webhook'),
    path('invoice/', views.StripeInvoiceView.as_view(), name='invoice'),
    path('intent/', views.SetupIntentView.as_view(), name='set_up_intent')
]
