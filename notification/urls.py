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
    path('todo/list/', views.TodoListView.as_view(), name='todo_list'),
    path('todo/<int:pk>', views.TodoCompletedView.as_view()),
    path('todo/item/return', views.TodoReturnItemView.as_view()),
    path('todo/item/purchased/<uuid:pk>', views.TodoPurchasedView.as_view())
]