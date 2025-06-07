from django.urls import path, include
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gin.urls')),
    #path('api/', include('inscription.urls')),
    path('api/', include('stages.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/realisations/', include('realisations.urls')),
    path('api/', include('partenaires.urls')),



    # JWT Authentication
   # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Configuration pour servir les fichiers media en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)