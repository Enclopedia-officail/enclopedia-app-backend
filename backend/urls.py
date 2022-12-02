from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
import debug_toolbar

def trigger_error(request):
    devision_by_zero = 1 / 0

urlpatterns = [
    path('enclopedia-administrator-operation/', admin.site.urls),
    path('api/product/', include('product.urls')),
    path('api/account', include('user.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('api/social_login/', include('social_login.urls')),
    path('api/stripe/', include('subscription.urls')),
    path('api/search/', include('category.urls')),
    path('api/history/', include('account_history.urls')),
    path('api/closet/', include('closet.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/reservation/', include('reservation.urls')),
    path('api/notification/', include('notification.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/password_reset/',
         include('django_rest_passwordreset.urls'), name='password_reset'),
    path('sentry-debug/', trigger_error),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
