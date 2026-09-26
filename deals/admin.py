from django.contrib import admin
from .models import Deal


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['strategy', 'deal_type', 'pair', 'from_price', 'to_price', 'is_followed_rules', 'result', 'created_at', 'updated_at']
    list_display_links = ['strategy', 'deal_type']
    search_fields = ['strategy', 'dealt_type', 'pair', 'description']
    list_filter = ['strategy', 'deal_type', 'pair', 'is_followed_rules', 'result']
