from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Category, City, Location, Event, EventList
from .serializers import (CitySerializer, CategorySerializer,
                          LocationSerializer, EventSerializer,
                          EventListSerializer)


class CityAPIView(APIView):
    """Представление города"""
    permission_classes = (IsAdminUser, )

    def get(self, request, *args, **kwargs):
        """Получить конкретный город или 
        список всех городов"""
        pk = kwargs.get("pk", None)

        if pk:
            city = City.objects.get(pk=pk)
            return Response({'city': CitySerializer(city).data})
        else:
            cities = City.objects.all()
            return Response({'cities': CitySerializer(cities, many=True).data})

    def post(self, request):
        """Создать город"""
        serializer = CitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'city': serializer.data})

    def put(self, request, *args, **kwargs):
        """Поменять город"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "method PUT not allowed!"})

        try:
            instance = City.objects.get(pk=pk)
        except:
            return Response({"error": "City does not exists!"})

        serializer = CitySerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'city': serializer.data})

    def delete(self, request, *args, **kwargs):
        """Удалить город"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"Ошибка": "Выберите правильный город!"})

        try:
            instance = City.objects.get(pk=pk)
            instance.delete()
            return Response({"Успех": "Город удален!",}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"Ошибка": "Город не существует!"})


class CategoryViewSet(viewsets.ModelViewSet):
    """Представление категорий мероприятий.
    CRUD операции с мероприятиями"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser, )


class EventViewSet(viewsets.ModelViewSet):
    """Представление событий. CRUD операции
    с событиями"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        """Для администратора доступны все
        права. Для обычного пользователя
        доступен только метод GET
        """
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update':
            permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class LocationViewSet(viewsets.ModelViewSet):
    """Представление локаций мероприятий"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (IsAdminUser, )

    def create(self, request):
        """Создать локацию"""
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'location': serializer.data})

    def update(self, request, *args, **kwargs):
        """Обновить локацию"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"Ошибка": "Неверно выбрана локация!"})

        try:
            instance = Location.objects.get(pk=pk)
        except:
            return Response({"Ошибка": "Локация не существует!"})

        serializer = LocationSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'location': serializer.data})


class EventListViewSet(viewsets.ModelViewSet):
    """Представление списка всех событий по
    датам и времени"""
    queryset = EventList.objects.all()
    serializer_class = EventListSerializer

    def get_permissions(self):
        """Для администратора доступны все
        права. Для обычного пользователя
        доступен только метод GET
        """
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update':
            permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def create(self, request):
        """Создать событие в конкретное время"""
        serializer = EventListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'new_event': serializer.data})

    def update(self, request, *args, **kwargs):
        """Поменять событие"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"Ошибка": "Неверно выбрано событие!"})

        try:
            instance = EventList.objects.get(pk=pk)
        except:
            return Response({"Ошибка": "Событие не существует!"})

        serializer = EventListSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'event': serializer.data})
