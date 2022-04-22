from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('dash/', include('adminpanel.urls')),
]

admin.site.site_header = 'WebStore Admin'
admin.site.site_title = 'Webstore Portal'
admin.site.index_title = 'Django WebStore'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)