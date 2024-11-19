from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('abi/', include('abi.urls')),
    path('', include('django_dyn_dt.urls')),  # <-- Dynamic_DT Routing
    path('', include('admin_abi.urls')),  
]

try:
    urlpatterns.append(path("login/jwt/", view=obtain_auth_token))
except:
    pass
