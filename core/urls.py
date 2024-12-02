from django.contrib import admin
from django.urls import include, path
from django.conf.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('abi/', include('abi.urls')),
    path('', include('admin_abi.urls')),  
]


handler404 = "abi.views.page_not_found"
handler403 = "abi.views.error_403"