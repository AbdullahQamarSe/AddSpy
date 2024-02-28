from django.contrib import admin
from .models import userauthenticate, Visitor

@admin.register(userauthenticate)
class UserAuthenticateAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_subscribe', 'counter', 'subscription_id')
    search_fields = ('email', 'name')
    list_filter = ('is_subscribe',)

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'country_name', 'coordinates', 'timestamp')
    search_fields = ('ip_address', 'country_name')
    list_filter = ('country_name', 'timestamp')
