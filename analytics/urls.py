from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('feature/', views.FeatureListView.as_view(), name='analytics_feature'),
    path('feature_brand/', views.FeatureBrandListView.as_view(), name='featured_brand'),
    path('test/', views.GooglaAnalyticsView.as_view(), name='analytics_popular'),
    path('view/', views.GoogleAnalyticsGA4.as_view(), name='get_item')
]