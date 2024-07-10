from django.contrib import admin

# Register your models here.

from .models import TimeSlot, Reservation, Profile, Cuisine, Order

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'cuisine', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'cuisine__name']

admin.site.register(TimeSlot)
admin.site.register(Reservation)
admin.site.register(Profile)