from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from events_app.views import *


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/cities/', CityAPIView.as_view()),
    path('api/v1/cities/<int:pk>/', CityAPIView.as_view()),
    path('api/v1/', include(router.urls))
]
