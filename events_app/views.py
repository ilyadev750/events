from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Category, City, Location, Event, EventList
from .serializers import (CitySerializer, CategorySerializer,
                          LocationSerializer, EventSerializer,
                          EventListSerializer)


class CityAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)

        if pk:
            city = City.objects.get(pk=pk)
            return Response({'city': CitySerializer(city).data})
        else:
            cities = City.objects.all()
            return Response({'cities': CitySerializer(cities, many=True).data})
    
    def post(self, request):
        serializer = CitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'city': serializer.data})

    def put(self, request, *args, **kwargs):
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
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"Ошибка": "Выберите правильный город!"})
        
        try:
            instance = City.objects.get(pk=pk)
            instance.delete()
            return Response({"Успех": "Город удален!"})
        except:
            return Response({"Ошибка": "Город не существует!"})
        

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, )


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'location': serializer.data})
    
    def update(self, request, *args, **kwargs):
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
    queryset = EventList.objects.all()
    serializer_class = EventListSerializer

    def create(self, request):
        serializer = EventListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'new_event': serializer.data})
    
    def update(self, request, *args, **kwargs):
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