from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Each app owns its own urls.py. We include them here under /api/.
    # This keeps the root urls.py clean and makes each app independently navigable.
    path('api/auth/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
]

# In development, Django itself serves uploaded media files (product images).
# In production you'd offload this to a CDN or Nginx — but for dev this is fine.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
