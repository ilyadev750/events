from rest_framework import routers
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from events_app.views import *
from users_app.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
   openapi.Info(
      title="Events API",
      default_version='v1',
      description="API testing",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'events', EventViewSet)
router.register(r'events-list', EventListViewSet)
router.register(r'events-registration', EventRegistrationViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/cities/', CityAPIView.as_view()),
    path('api/v1/cities/<int:pk>/', CityAPIView.as_view()),
    path('api/v1/', include(router.urls)),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('users_app.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
