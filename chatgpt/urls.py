from django.urls import path
from . import views

app_name = 'chatgpt'

urlpatterns = [
    path('image/', views.CreateImageView.as_view()),
]