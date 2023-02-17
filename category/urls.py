from django.urls import path
from . import views
from django.views.decorators.cache import cache_page as view_cache_page

TIME_OUT_HOUR = 60 * 60
TIME_OUTS_1DAY = 60 * 60 * 24
TIME_OUTS_1MONTH = TIME_OUTS_1DAY * 30


def cache_page(view, timeouts=TIME_OUTS_1DAY):
    return view_cache_page(timeouts)(view)


app_name = 'category'
urlpatterns = [
    path('category/list/',
        cache_page(views.CategorySearchListView.as_view(), TIME_OUTS_1DAY), name='category_list'),
    path('category/<slug:slug>/',
         views.CategorySearchView.as_view(), name='category_detail'),
    path('type/list/', cache_page(views.TypeListView.as_view(), TIME_OUTS_1DAY), name='type_list'),
    path('type/', cache_page(views.CategoryListView.as_view(), TIME_OUTS_1DAY), name='category_list'),
    path('brand/list/', cache_page(views.BrandView.as_view(), TIME_OUTS_1DAY), name='brand_list'),
    path('brand/<slug:slug>/', cache_page(views.BrandSearchView.as_view(), TIME_OUT_HOUR), name='brand_product'),
]
