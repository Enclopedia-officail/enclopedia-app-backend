from django.urls import path, include
from django.urls.resolvers import URLPattern
from .views import GoogleLoginView, RefreshTokenView

urlpatterns = [
    path('google/', GoogleLoginView.as_view(), name='socialaccount_signup'),
]
