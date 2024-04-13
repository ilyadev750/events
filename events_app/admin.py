from django.contrib import admin
from .models import Category, Location, City, Event, EventList


admin.site.register(Category)
admin.site.register(Location)
admin.site.register(City)
admin.site.register(Event)
admin.site.register(EventList)


