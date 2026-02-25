from django.contrib import admin

from .models import Category, Order, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "available", "created")
    list_filter = ("available", "created", "updated", "category")
    list_editable = ("price", "stock", "available")
    search_fields = ("name", "category__name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "first_name",
        "last_name",
        "total_paid",
        "created",
    )
    list_filter = ("created",)
    search_fields = ("first_name", "last_name", "email", "user__username")
