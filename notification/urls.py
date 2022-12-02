from django.urls import path
from . import views

app_name='notification'

urlpatterns = [
    path('read/list/', views.ReadListView.as_view(), name='read'),
    path('read/update', views.AlreadyReadView.as_view(), name='read_update'),
    path('news/list/', views.NewsListView.as_view(), name='news'),
    path('list/', views.NotificationListView.as_view(), name='notifiaction'),
    path('news/<int:pk>/', views.NewsView.as_view()),
    path('<int:pk>/', views.NotificationRetreiveView.as_view()),
]