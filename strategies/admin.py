from django.contrib import admin
from .models import Strategy


@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'balance', 'created_at', 'updated_at']
    list_filter = ['user', 'balance']
    search_fields = ['user', 'title', 'rules']
    list_display_links = ['user', 'title']
    
