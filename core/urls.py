from django.contrib import admin
from django.urls import include, path
from django.conf.urls import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('abi/', include('abi.urls')),
    path('', include('admin_abi.urls')),  
]


handler404 = "abi.views.page_not_found"
handler403 = "abi.views.error_403"

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)