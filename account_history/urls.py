from django.urls import path
from . import views
from django.views.decorators.cache import cache_page as view_cache_page

app_name = 'account_history'

TIME_OUTS_MINUTE = 60 * 3
TIME_OUTS_1DAY = 60 * 60 * 24
TIME_OUTS_1MONTH = TIME_OUTS_1DAY * 30


def cache_page(view, timeouts=TIME_OUTS_MINUTE):
    return view_cache_page(timeouts)(view)


urlpatterns = [
    #path('/browsing/', )
    path('favorite/', views.FavoriteGetView.as_view(), name='favorite_get'),
    path('favorite/create/', views.FavoriteCreateView.as_view(),
         name='favorite_create'),
    path('favorite/list/',
         views.FavoriteListView.as_view(), name='favorite'),
    path('favorite/update/', views.FavoriteUpdateView.as_view()),
    path('favorite/delete/<int:pk>', views.FavoriteDeleteView.as_view(),
         name='favorite_delete'),
    path('browsing', views.BrowsingHistoryView.as_view()),
    path('search_word', views.SearchHistoryView.as_view())
]
