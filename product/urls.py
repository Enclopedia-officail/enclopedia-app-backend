from django.urls import path
from . import views


from django.views.decorators.cache import cache_page as view_cache_page

TIME_OUT_MINUTES = 60
TIME_OURTS_MINUTES = 60 * 30
TIME_OUTS_HOUR = 60 * 60
TIME_OUTS_1DAY = 60 * 60 * 24


def cache_page(view, timeouts=TIME_OURTS_MINUTES):
    return view_cache_page(timeouts)(view)


app_name = 'product'

urlpatterns = [
    path('search/', cache_page(views.ProductSearch.as_view(), TIME_OUTS_HOUR), name='prduct_search'),
    path('search/evaluation_order/',
         cache_page(views.ProductSearchReviewListView.as_view(), TIME_OUTS_HOUR), name='search_evaluation'),
    path('search/evaluation_order_desc/', cache_page(views.ProductSearchReviewDescListView.as_view(), TIME_OUTS_HOUR),
         name='search_evaluation_desc'),
    path('search/favorite_order/',
         cache_page(views.ProductSearchFavoriteListView.as_view(), TIME_OUTS_HOUR), name='search_favorite'),
    path('search/favorite_order_desc/', cache_page(views.ProductSearchFavoriteDescListView.as_view(),TIME_OUTS_HOUR),
         name='search_favorite_desc'),
    path('search/reservation_order/', cache_page(views.ProductSearchOrderReservationView.as_view(), TIME_OUTS_HOUR), name='search_reservation_order'),
    path('search/reservation_order_desc/', cache_page(views.ProductSearchOrderReservationDescView.as_view(), TIME_OUTS_HOUR), name='search_reservation_order_desc'),
    path('search/price_order/', cache_page(views.ProductSearchPriceView.as_view(), TIME_OUTS_HOUR), name='search_price'),
    path('search/price_order_desc/', views.ProductSearchPriceDescView.as_view(), name='search_price_desc'),
    path('search/category/', cache_page(views.ProductSearchCategoryListView.as_view(), TIME_OUTS_HOUR),
         name="search_category"),
    path('search/type/', views.ProductSearchTypeListView.as_view(), name='search_type'),
    path('detail/<str:pk>/', views.ProductGetView.as_view(), name="product"),
    path('list/', cache_page(views.ProductListView.as_view(), TIME_OUTS_HOUR), name="product-list"),
    path('evaluation_order/', cache_page(views.ProductReviewListView.as_view(), TIME_OUTS_HOUR),
         name='evaluation_order'),
    path('evaluation_order/desc/', cache_page(views.ProductReviewDescListView.as_view(), TIME_OUTS_HOUR),
         name='evaluation_order_desc'),
    path('favorite_order/', cache_page(views.FavoriteProductView.as_view(),  TIME_OUTS_HOUR),
         name='favorite_order'),
    path('favorite_order/desc/', cache_page(views.FavoriteProductDescView.as_view(),TIME_OUTS_HOUR),
         name='favorite_order_desc'),
    path('reservation_order/', cache_page(views.ProductOrderReservationView.as_view(), TIME_OUTS_HOUR), name='reservation_order_product'),
    path('reservation_order/desc/', cache_page(views.ProductOrderDescReservationView.as_view(),TIME_OUTS_HOUR), name='reservation_order_desc_product'),
    path('price_order/', cache_page(views.ProductPriceOrderView.as_view(), TIME_OUTS_HOUR), name="price_order"),
    path('price_order_desc/', cache_page(views.ProductPriceDescOrderView.as_view(), TIME_OUTS_HOUR), name="price_order_desc"),
    path('type/', cache_page(views.ProductTypeView.as_view(), TIME_OUTS_HOUR), name='product_tyoe'),
    path('brand/', cache_page(views.ProductBrandView.as_view(), TIME_OUTS_HOUR), name='brand_product'),
    path('brand/evaluation_order/',
         cache_page(views.ProductBrandReviewListView.as_view(), TIME_OUTS_HOUR), name='brand_evaluation'),
    path('brand/evaluation_order_desc/',
         cache_page(views.ProductBrandReviewDescListView.as_view(), TIME_OUTS_HOUR), name='brand_evaluation_desc'),
    path('brand/favorite_order/',
          cache_page(views.ProducBrandFavoriteView.as_view(), TIME_OUTS_HOUR), name='brand_favorite'),
    path('brand/favorite_order_desc/',
          cache_page(views.ProducBrandFavoriteDescView.as_view(), TIME_OUTS_HOUR), name='brand_favorite_desc'),
    path('brand/reservation_order/', cache_page(views.ProductBrandReservationView.as_view(),TIME_OUTS_HOUR), name='brand_reservation'),
    path('brand/reservation_order_desc/', cache_page(views.ProductBrandReservationDescView.as_view(),TIME_OUTS_HOUR), name='brand_reservation_desc'),
    path('brand/category/', cache_page(views.ProductBrandCategoryView.as_view(),TIME_OUTS_1DAY),
         name='brand_category'),
    path('brand/type/', cache_page(views.ProductBrandTypeView.as_view(), TIME_OUTS_HOUR), name='brand_type'),
    path('brand/price_order/', cache_page(views.ProductBrandPriceView.as_view(), TIME_OUTS_HOUR), name='brand_price'),
    path('brand/price_order_desc/', cache_page(views.ProductBrandPriceDescView.as_view(), TIME_OUTS_HOUR), name='brand_price_desc'),
    path('variation/<uuid:product>/',
         views.VariationGetView.as_view(), name="variation"),
    path('images/<uuid:product>/',
         views.ImageGallaryView.as_view(), name='image_gallary'),
    path('category/<str:category>/',
         views.ProductCategoryView.as_view(), name='category_prodcut'),
    path('size/<uuid:product>/', cache_page(views.ProductSizeView.as_view(),TIME_OUTS_1DAY), name='size'),
    path('reviews/<uuid:product>/', views.ReviewList.as_view(), name='reviews'),
    path('review/list/<uuid:product>/',
         views.ReviewRatingView.as_view(), name='review'),
    path('review/create/<uuid:product>', views.ReviewRatingCreateView.as_view(),
         name='review_create'),
    path('review/user/<uuid:pk>/', views.UserReview.as_view(), name='user_review'),
    path('tag/', cache_page(views.ProductTagListView.as_view(), TIME_OUTS_1DAY), name="product_tag"),
    path('tag/evaluation_order/',
         cache_page(views.ProudctTagRatingView.as_view(), TIME_OUTS_HOUR), name="tag_evaluate"),
    path('tag/evaluation_order_desc/',
         cache_page(views.ProductTagRatingDescView.as_view(), TIME_OUTS_HOUR), name="tag_evaluate_desc"),
    path('tag/favorite/', cache_page(views.ProductTagFavoriteView.as_view(),TIME_OUTS_HOUR), name="tag_favorite"),
    path('tag/favorite_desc/', cache_page(views.ProductTagFavoriteDescView.as_view(), TIME_OUTS_HOUR),
         name="tag_favorite_desc"),
    path('tag/reservation_order/', cache_page(views.ProductTagReservationView.as_view(), TIME_OUTS_HOUR)),
    path('tag/reservation_order_desc/', cache_page(views.ProductTagReservationDescView.as_view(), TIME_OUTS_HOUR)),
    path('tag/category/', cache_page(views.ProductTagCategoryView.as_view(), TIME_OUTS_HOUR), name="tag_category"),
    path('tag/type/', cache_page(views.ProductTagTypeView.as_view(), TIME_OUTS_HOUR), name='tag_type'),
    path('tag/price_order/', cache_page(views.ProductTagPriceOrderView.as_view(), TIME_OUTS_HOUR), name="tag_price_order"),
    path('tag/price_order_desc/', cache_page(views.ProductTagPriceOrderDescView.as_view(), TIME_OUTS_HOUR), name="tag_price_order_desc"),
    path('tag/list/', views.TagListProductGetView.as_view()),
    path('tag/search/', views.TagListAPIVIew.as_view()),
    path('related/', views.RelatedProductListViwe.as_view(), name='related_product'),
    path('search_word/', views.SearchWordView.as_view()),
]
