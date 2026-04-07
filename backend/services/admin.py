from django.contrib import admin
from .models import Category, Service

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'provider',
        'category',
        'pricing_type',
        'price',
        'is_active',
        'created_at',
    )
    list_filter = ('category', 'pricing_type', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'provider__username')
