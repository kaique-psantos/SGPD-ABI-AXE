
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token # <-- NEW

urlpatterns = [
    path('abi/', include('abi.urls')),
    path("admin/", admin.site.urls),
    path("", include('admin_datta.urls')),
    path('', include('django_dyn_dt.urls')), # <-- NEW: Dynamic_DT Routing   
]

# Lazy-load on routing is needed
# During the first build, API is not yet generated
try:
    urlpatterns.append( path("login/jwt/", view=obtain_auth_token) )
except:
    pass
