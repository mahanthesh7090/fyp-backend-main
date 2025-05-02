from django.contrib import admin
from .models import Tweet, City, Location
# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    list_display = ('tweet', 'city', 'problem_type')
    list_filter = ('city', 'problem_type')
admin.site.register(Tweet, TweetAdmin)

class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(City, CityAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location', 'tweet')
    list_filter = ('location', 'tweet')
admin.site.register(Location, LocationAdmin)