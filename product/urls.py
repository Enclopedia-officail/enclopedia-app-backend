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
    path('search/', cache_page(views.ProductSearch.as_view(), TIME_OUTS_1DAY), name='prduct_search'),
    path('search/evaluation_order/',
         cache_page(views.ProductSearchReviewListView.as_view(), TIME_OUTS_1DAY), name='search_evaluation'),
    path('search/evaluation_order_desc/', cache_page(views.ProductSearchReviewDescListView.as_view(), TIME_OUTS_1DAY),
         name='search_evaluation_desc'),
    path('search/favorite_order/',
         views.ProductSearchFavoriteListView.as_view(), name='search_favorite'),
    path('search/favorite_order_desc/', views.ProductSearchFavoriteDescListView.as_view(),
         name='search_favorite_desc'),
    path('search/reservation_order/', views.ProductSearchOrderReservationView.as_view(), name='search_reservation_order'),
    path('search/reservation_order_desc/', views.ProductSearchOrderReservationDescView.as_view(), name='search_reservation_order_desc'),
    path('search/price_order/', views.ProductSearchPriceView.as_view(), name='search_price'),
    path('search/price_order_desc/', views.ProductSearchPriceDescView.as_view(), name='search_price_desc'),
    path('search/category/', cache_page(views.ProductSearchCategoryListView.as_view(), TIME_OUTS_1DAY),
         name="search_category"),
    path('search/type/', views.ProductSearchTypeListView.as_view(), name='search_type'),
    path('detail/<str:pk>/', views.ProductGetView.as_view(), name="product"),
    path('list/', views.ProductListView.as_view(), name="product-list"),
    path('evaluation_order/', views.ProductReviewListView.as_view(),
         name='evaluation_order'),
    path('evaluation_order/desc/', views.ProductReviewDescListView.as_view(),
         name='evaluation_order_desc'),
    path('favorite_order/', views.FavoriteProductView.as_view(),
         name='favorite_order'),
    path('favorite_order/desc/', views.FavoriteProductDescView.as_view(),
         name='favorite_order_desc'),
    path('reservation_order/', views.ProductOrderReservationView.as_view(), name='reservation_order_product'),
    path('reservation_order/desc/', views.ProductOrderDescReservationView.as_view(), name='reservation_order_desc_product'),
    path('price_order/', views.ProductPriceOrderView.as_view(), name="price_order"),
    path('price_order_desc/', views.ProductPriceDescOrderView.as_view(), name="price_order_desc"),
    path('type/', views.ProductTypeView.as_view(), name='product_tyoe'),
    path('brand/', views.ProductBrandView.as_view(), name='brand_product'),
    path('brand/evaluation_order/',
         views.ProductBrandReviewListView.as_view(), name='brand_evaluation'),
    path('brand/evaluation_order_desc/',
         views.ProductBrandReviewDescListView.as_view(), name='brand_evaluation_desc'),
    path('brand/favorite_order/',
          views.ProducBrandFavoriteView.as_view(), name='brand_favorite'),
    path('brand/favorite_order_desc/',
          views.ProducBrandFavoriteDescView.as_view(), name='brand_favorite_desc'),
    path('brand/reservation_order/', views.ProductBrandReservationView.as_view(), name='brand_reservation'),
    path('brand/reservation_order_desc/', views.ProductBrandReservationDescView.as_view(), name='brand_reservation_desc'),
    path('brand/category/', cache_page(views.ProductBrandCategoryView.as_view(),TIME_OUTS_1DAY),
         name='brand_category'),
    path('brand/type/', views.ProductBrandTypeView.as_view(), name='brand_type'),
    path('brand/price_order/', views.ProductBrandPriceView.as_view(), name='brand_price'),
    path('brand/price_order_desc/', views.ProductBrandPriceDescView.as_view(), name='brand_price_desc'),
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
         views.ProudctTagRatingView.as_view(), name="tag_evaluate"),
    path('tag/evaluation_order_desc/',
         views.ProductTagRatingDescView.as_view(), name="tag_evaluate_desc"),
    path('tag/favorite/', views.ProductTagFavoriteView.as_view(), name="tag_favorite"),
    path('tag/favorite_desc/', views.ProductTagFavoriteDescView.as_view(),
         name="tag_favorite_desc"),
    path('tag/reservation_order/', views.ProductTagReservationView.as_view()),
    path('tag/reservation_order_desc/', views.ProductTagReservationDescView.as_view()),
    path('tag/category/', views.ProductTagCategoryView.as_view(), name="tag_category"),
    path('tag/type/', views.ProductTagTypeView.as_view(), name='tag_type'),
    path('tag/price_order/', views.ProductTagPriceOrderView.as_view(), name="tag_price_order"),
    path('tag/price_order_desc/', views.ProductTagPriceOrderDescView.as_view(), name="tag_price_order_desc"),
    path('tag/list/', views.TagListProductGetView.as_view()),
    path('related/', views.RelatedProductListViwe.as_view(), name='related_product'),
    path('search_word/', views.SearchWordView.as_view()),
]
