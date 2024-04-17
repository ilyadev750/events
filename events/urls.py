from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from events_app.views import *
from users_app.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('users_app.urls'))
]
